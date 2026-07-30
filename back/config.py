from dotenv import load_dotenv
import os
import boto3
import json

class Settings():
    DB_URL = os.getenv("DB")
    DEBUG = True


settings = Settings()