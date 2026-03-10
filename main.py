from fastapi import Depends, Request
from fastapi import UploadFile, File, Form
from models import Webhook, Audio, AudioStatus
from db_services import DBService
import asyncpg
import json
import requests
from fastapi import FastAPI, UploadFile, File
import os
from datetime import datetime
import logging
import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a"
)
logger = logging.getLogger(__name__)

app = FastAPI()

UPLOAD_DIR = datetime.now().strftime("%d_%m_%Y")
os.makedirs(UPLOAD_DIR, exist_ok=True)

DATABASE_URL = "postgresql://bank:bank@localhost:5432/bank"

db_pool = None

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await db_pool.close()

async def get_db():
    return DBService(db_pool)


@app.post("/webhook")
async def webhook_handler(request: Request, db: DBService = Depends(get_db)):
    webhook_id = None
    try:
        data = await request.json()

        webhook_id = data.get("id", 1)
        branch_id = data.get("branchId", 1)
        workstation_id = data.get("workstationId", 1)
        action = data.get("data", {}).get("actionType", "NoAction")

        logger.info(f"webhook id: {webhook_id} branch_id: {branch_id} workstation_id: {workstation_id} action: {action}")
        operator = await db.get_operator_by_workstation_id(workstation_id)

        if action == "Accept":
            webhook = Webhook(
                id=webhook_id,
                branch_id=branch_id,
                workstation_id=workstation_id,
                rawdata = json.dumps(data)
            )

            await db.insert_webhook(webhook)

            audio = Audio(
                operator_id=operator.id,
                webhook_id=webhook.id,
                status=AudioStatus.started
            )
            await db.insert_audio(audio)

            url = f"http://{operator.laptop_ip}:{operator.laptop_port}/start"
            async with httpx.AsyncClient() as client:
                response = await client.post(url, params={"record_id": webhook_id})

            res_data = response.json()
            print(res_data)

            if res_data["status_code"] == 200:
                logger.info(f"webhook id: {webhook_id} audio recording started")
                return {"status": "started"}
            elif res_data["status_code"] == 201:
                audio.status = AudioStatus.not_detected
                await db.update_audio(audio)
                logger.info(f"webhook id: {audio.id} {webhook_id} audio recording not started, because microphone no detected")
                return {"status": res_data["status"]}

            return {"status": res_data["status"]}
        elif action == "End":
            audio = await db.get_audio_by_webhook_id(webhook_id)
            if not audio:
                return {"status": f"{webhook_id} audio not started"}
            url = f"http://{operator.laptop_ip}:{operator.laptop_port}/stop"
            async with httpx.AsyncClient() as client:
                response = await client.post(url)

            audio.status = AudioStatus.stopped
            await db.update_audio(audio)

            if response.status_code == 200:
                logger.info(f"webhook id: {webhook_id} audio recording succesfully ended")
                return {"status": "Success to stop audio recording"}
            return {"status": "An error occured processing audio recording succesfully ended"}
    except Exception as e:
        logger.exception(f"Webhook processing error. webhook_id={webhook_id}")
        return {"status": "error", "message": str(e)}

    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), record_id: str = Form(...), db: DBService = Depends(get_db)):
    filename = f"{file.filename}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)  # 1MB chunk
            if not chunk:
                break
            f.write(chunk)
    audio = await db.get_audio_by_webhook_id(int(record_id))
    print(file_path)
    audio.audio = str(file_path)
    audio.status = AudioStatus.uploaded
    await db.update_audio(audio)

    logging.info(f"File saved: {filename} record_id={record_id}")

    return {
        "status_code": 200,
        "status": "saved",
        "record_id": record_id,
        "filename": filename
    }