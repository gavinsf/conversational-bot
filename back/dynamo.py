from contextlib import asynccontextmanager
from back.config import settings
import aioboto3

TABLE_NAME = "messages"

session = aioboto3.Session()

_dynamo_ctx = None
_table = None

@asynccontextmanager
async def get_table():
    global _dynamo_ctx, _table

    if _table is None:
        _dynamo_ctx = session.resource("dynamodb", region_name=settings.AWS_REGION)
        resource = await _dynamo_ctx.__aenter__()
        _table = await resource.Table(TABLE_NAME)
    yield _table


async def close_table():
    global _dynamo_ctx, _table
    if _dynamo_ctx is not None:
        await _dynamo_ctx.__aexit__(None, None, None)
        _dynamo_ctx = None
        _table = None
