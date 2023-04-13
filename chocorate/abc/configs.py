from os import environ
from pydantic import BaseModel
from dotenv import load_dotenv


class Config(BaseModel):
    token_url: str = "token"


config = Config()

load_dotenv()
APP_SECRET = environ["CHOCO_SECRET_KEY"]


    