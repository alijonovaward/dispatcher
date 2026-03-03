import asyncpg
from typing import List
from models import Webhook, Operator, Audio

class DBService:
    def __init__(self, pool: asyncpg.pool.Pool):
        self.pool = pool

    # --- Webhook ---
    async def insert_webhook(self, webhook: Webhook):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO webhooks (id, branch_id, workstation_id, rawdata) VALUES ($1,$2,$3,$4)",
                webhook.id, webhook.branchId, webhook.workstationId, webhook.rawdata
            )

    async def get_webhooks(self) -> List[Webhook]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM webhooks")
            return [Webhook(**dict(row)) for row in rows]

    # --- Operators ---
    async def insert_operator(self, operator: Operator):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO operators (id, branch_id, workstation_id, laptop_ip, laptop_port) VALUES ($1,$2,$3,$4,$5)",
                operator.id, operator.branchId, operator.workstationId, operator.laptopIp, operator.laptopPort
            )

    async def get_operators(self) -> List[Operator]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM operators")
            return [Operator(**dict(row)) for row in rows]

    # --- Audio ---
    async def insert_audio(self, audio: Audio):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO audio (id, operator_id, audio, status) VALUES ($1,$2,$3,$4)",
                audio.id, audio.operatorId, audio.audio, audio.status.value
            )

    async def get_audios(self) -> List[Audio]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM audio")
            return [Audio(**dict(row)) for row in rows]