from dotenv import load_dotenv
import os
import aioboto3

load_dotenv()

class Settings():
    DB_URL = os.getenv("DB")
    DEBUG = True
    BOT_ID = os.getenv("LEX_BOT_ID")
    BOT_ALIAS_ID = os.getenv("LEX_BOT_ALIAS_ID")
    LOCALE_ID = os.getenv("LEX_LOCALE_ID")
    AWS_REGION = os.getenv("AWS_REGION")
    session = aioboto3.Session()


settings = Settings()