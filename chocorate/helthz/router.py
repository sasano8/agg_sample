from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse


router = APIRouter()


# healthz/


@router.get("/liveness", response_class=PlainTextResponse)
def liveness():
    return "alive"


@router.get("/readiness", response_class=PlainTextResponse)
def readiness():
    return "ready"


# @router.get("/startup", response_class=PlainTextResponse)
# def startup():
#     return "start"
