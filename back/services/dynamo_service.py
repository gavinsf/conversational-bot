from back.schemas import ChatInput
from back.dynamo import get_table
from back.models.log_models import MessageLog
from fastapi import HTTPException

async def log_message(message: MessageLog):
    table = await get_table()
    try:
        table.put_item(MessageLog=message.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_message(session_id: str):
    table = await get_table()
    response = table.get_item(
        Key={"session_id": session_id}
    )
    return response.get("MessageLog")