import uuid
from fastapi import Response

async def create_session_id(response: Response):
    session_id = str(uuid.uuid4())
    response.set_cookie(
        key="session_id",
        value=session_id,
        secure=True,
        httponly=True,
        max_age = 60 * 60 * 24
    )