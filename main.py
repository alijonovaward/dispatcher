from fastapi import FastAPI, Depends, Request
from models import Webhook
from db_services import DBService
import asyncpg
import httpx

app = FastAPI()

DATABASE_URL = "postgresql://bank:bank@localhost:5432/bank"


# --- DB pool ---
async def get_db():
    pool = await asyncpg.create_pool(DATABASE_URL)
    return DBService(pool)


@app.post("/webhook")
async def webhook_handler(request: Request, db: DBService = Depends(get_db)):
    data = await request.json()

    branch_id = data["branchId"]
    workstation_id = data["workstationId"]
    action = data["data"]["actionType"]

    if action == "Accept":
        await db.insert_webhook()
    elif action == "End":
        pass

    await db.insert_webhook(data)

    # 2️⃣ Operator topish
    operators = await db.get_operators()

    operator = None
    for op in operators:
        if op.branch_id == data.branch_id and op.workstation_id == data.workstation_id:
            operator = op
            break

    if not operator:
        return {"status": "operator not found"}

    url = f"http://{operator.laptopIp}:{operator.laptopPort}/{action}"

    # 4️⃣ Operator kompyuterga request yuborish
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url)

        return {
            "status": "sent",
            "operator": operator.id,
            "action": action,
            "response": response.text
        }

    except Exception as e:
        return {"status": "error", "detail": str(e)}