from back.schemas import ChatInput
from back.dynamo import get_table
from fastapi import HTTPException

async def log_message(session_id: str, text: str):
    async with get_table() as table:
        try:
            await table.put_item(Item={"session_id":session_id, "text":text})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


async def get_message(session_id: str):
    async with get_table() as table:
        response = await table.get_item(
            Key={"session_id": session_id}
        )
        return response.get("Item")