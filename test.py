import asyncio
import asyncpg
from models import Webhook, Operator, Audio, AudioStatus
from db_services import DBService

DATABASE_URL = "postgresql://bank:bank@localhost:5432/bank"

async def main():
    # 1️⃣ DB Pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    db = DBService(pool)

    # # 2️⃣ Webhook insert va select
    # webhook = Webhook(id=5, branch_id=101, workstation_id=201, rawdata="raw data test")
    # await db.insert_webhook(webhook)
    # webhooks = await db.get_webhooks()
    # print("Webhooks:", webhooks)

    # 3️⃣ Operator insert va select
    # operator = Operator(branch_id=101, workstation_id=203, laptop_ip="192.168.1.10", laptop_port=8080)
    # await db.insert_operator(operator)
    # operators = await db.get_operators()
    # print("Operators:", operators)

    # 4️⃣ Audio insert va select
    audio = Audio(operator_id=1, webhook_id=5, status=AudioStatus.started)
    await db.insert_audio(audio)
    audios = await db.get_audios()
    print("Audios:", audios)

    await pool.close()

asyncio.run(main())