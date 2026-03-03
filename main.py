from fastapi import FastAPI, Depends, Request
from models import Webhook, Audio, AudioStatus
from db_services import DBService
import asyncpg
import httpx
import json

app = FastAPI()

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

    if action == "Accept":
        webhook = Webhook(
            id=data["id"],
            branch_id=branch_id,
            workstation_id=workstation_id,
            rawdata = json.dumps(data)
        )

        is_created = await db.get_webhook_by_id(webhook.id)
        # if is_created:
        #     return {"status": "already exist"}

        await db.insert_webhook(webhook)
        operator = await db.get_operator_by_workstation_id(workstation_id)

        audio = Audio(
            id=data["id"],
            operator_id=operator.id,
            audio="file path",
            status=AudioStatus.started
        )
        await db.insert_audio(audio)

        return {"status": "created", "operator": operator}
    elif action == "End":
        return {"actionType" : "End"}

    return {"status": "ok"}