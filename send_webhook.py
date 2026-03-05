import httpx
import asyncio
import json

async def send_webhook():
    url = "http://127.0.0.1:8000/webhook"
    data = {
    "id": 200718023,
    "number": "O1",
    "createDate": "2026-02-25T08:20:46.533",
    "branchId": 511,
    "queueType": "Оплата комунальных услуг",
    "externalTicketIds": None,
    "ticketQRGuid": None,
    "branchName": "Центр банковских услуг \"Коканд\"",
    "terminalId": 1000368,
    "ticketId": 200718023,
    "action": 8,
    "clientId": "",
    "data": {
        "actionType": "End",
        "ticketStatus": "Finished",
        "date": "02/25/2026 08:20:50",
        "clientId": None,
        "branch": "Центр банковских услуг \"Коканд\"",
        "employee": "queue_inspector queue_inspector",
        "printDate": "02/25/2026 08:20:46",
        "callDate": "02/25/2026 08:20:46",
        "employeeEmail": None
    },
    "queueTypeId": 5330,
    "workstationId": 2946,
    "languageIsoCode": "en-US",
    "externalCompanyId": "",
    "externalData": None,
    "workstationNumber": "1",
    "mobileData": None
}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data)
        print(response.status_code, response.text)

asyncio.run(send_webhook())