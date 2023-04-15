from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse

router = APIRouter()


@router.get("/volume/template", response_class=PlainTextResponse)
def volume_template():
    ...


@router.post("/volume/create")
def volume_create():
    ...


@router.delete("/volume/delete")
def volume_delete():
    ...


@router.get("/volume/list")
def volumne_list():
    ...


@router.get("/volume/list")
def volumne_detail():
    ...
