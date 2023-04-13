from fastapi import APIRouter, Depends
from typing_extensions import Annotated
from chocorate.abc import config
from fastapi.security import OAuth2PasswordBearer
from .views import User

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=config.token_url)


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@router.get("/users/me")
def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
