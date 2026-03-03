import httpx
import asyncio
import json

async def send_webhook():
    url = "http://127.0.0.1:8000/webhook"
    data ={
        "id": 200717968,
        "number": "A1",
        "createDate": "2026-02-25T08:20:33.097",
        "branchId": 511,
        "queueType": "Консультация по кредиту",
        "externalTicketIds": None,
        "ticketQRGuid": None,
        "branchName": "Центр банковских услуг \"Коканд\"",
        "terminalId": 1000368,
        "ticketId": 200717966,
        "action": 7,
        "clientId": "",
        "data": {
            "actionType": "Accept",
            "ticketStatus": "Serving",
            "date": "02/25/2026 08:20:35",
            "clientId": None,
            "branch": "Центр банковских услуг \"Коканд\"",
            "employee": "queue_inspector queue_inspector",
            "printDate": "02/25/2026 08:20:33",
            "callDate": "02/25/2026 08:20:33",
            "employeeEmail": None
        },
        "queueTypeId": 1222,
        "workstationId": 201,
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