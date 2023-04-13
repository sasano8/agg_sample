from pydantic import BaseModel


class Config(BaseModel):
    token_url: str = "token"


config = Config()
