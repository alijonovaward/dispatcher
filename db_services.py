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
                webhook.id, webhook.branch_id, webhook.workstation_id, webhook.rawdata
            )

    async def get_webhooks(self) -> List[Webhook]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM webhooks")
            return [Webhook(**dict(row)) for row in rows]

    async def get_webhook_by_id(self, webhook_id: int) -> Webhook:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM webhooks WHERE id = $1", webhook_id)
            return Webhook(**dict(row)) if row else None

    # --- Operators ---
    async def insert_operator(self, operator: Operator):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO operators (id, branch_id, workstation_id, laptop_ip, laptop_port) VALUES ($1,$2,$3,$4,$5)",
                operator.id, operator.branch_id, operator.workstation_id, operator.laptop_ip, operator.laptop_port
            )

    async def get_operators(self) -> List[Operator]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM operators")
            return [Operator(**dict(row)) for row in rows]

    async def get_operator_by_workstation_id(self, workstation_id: int) -> Operator:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM operators WHERE workstation_id = $1", workstation_id)
            return Operator(**dict(row)) if row else None

    # --- Audio ---
    async def insert_audio(self, audio: Audio):
        async with self.pool.acquire() as conn:
            await conn.execute(
                "INSERT INTO audios (id, operator_id, audio, status) VALUES ($1,$2,$3,$4)",
                audio.id, audio.operator_id, audio.audio, audio.status.value
            )

    async def get_audios(self) -> List[Audio]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM audios")
            return [Audio(**dict(row)) for row in rows]