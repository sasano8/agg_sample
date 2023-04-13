from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse


ci_router = APIRouter()
queue_router = APIRouter()


@ci_router.get("/images")
def get_images():
    return {"hello-world", "nvidia/cuda"}


@ci_router.post("/tasks")
def add_task(
    image_name: str,
    repositry_url: str = "",
    asset_url: str = "",
    entry_point: str = "train:run",
):
    global QUEUE
    images = get_images()
    if image_name not in get_images():
        raise HTTPException(500, "Not Found Image")

    cmd = ["docker", "run", "--rm", image_name]
    QUEUE.append(cmd)
    return HTMLResponse(status_code=202)


@queue_router.get("/tasks")
def query_task():
    return [*QUEUE, *COMPLTED]


@queue_router.get("/tasks/{index}")
def get_task(index: int):
    queue = [*QUEUE, *COMPLTED]
    print(queue)
    row = queue[index]
    return PlainTextResponse(row["result"])


# application/problem+json
{
    "type": "https://example.com/probs/out-of-credit",
    "title": "You do not have enough credit.",
    "status": 500,
    "instance": "/account/12345/msgs/abc",
    "detail": "Your current balance is 30, but that costs 50.",
    # "invalid-params": []
    # "balance": 30,
    # "accounts": [
    # "/account/12345",
    #     "/account/67890"
    # ]
}
