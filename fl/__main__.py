import uvicorn


if __name__ == "__main__":
    uvicorn.run("fl.plugins.app:app", host="0.0.0.0")
