from fastapi import Depends, Request
from models import Webhook, Audio, AudioStatus
from db_services import DBService
import asyncpg
import httpx
import json
import requests
from fastapi import FastAPI, UploadFile, File
import os
from datetime import datetime


app = FastAPI()

UPLOAD_DIR = "received_files"
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
    data = await request.json()

    branch_id = data["branchId"]
    workstation_id = data["workstationId"]
    action = data["data"]["actionType"]
    operator = await db.get_operator_by_workstation_id(workstation_id)

    if action == "Accept":
        webhook = Webhook(
            id=data["id"],
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
        response = requests.post(url, params={"record_id": data["id"]})

        return {"status": "created", "audio": audio.id}
    elif action == "End":
        audio = await db.get_audio_by_webhook_id(data["id"])

        url = f"http://{operator.laptop_ip}:{operator.laptop_port}/stop"
        response = requests.post(url)

        audio.status = AudioStatus.stopped
        await db.update_audio(audio)



        return {"status": "stopped audio", "audio": audio.id}
    return {"status": "ok"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)  # 1MB chunk
            if not chunk:
                break
            f.write(chunk)

    return {
        "status": "saved",
        "filename": filename
    }