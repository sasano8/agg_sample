import subprocess


QUEUE = []
COMPLTED = []


def add_handler(app):
    import asyncio
    from asyncio import Task

    task: Task

    @app.on_event("startup")
    async def startup_event():
        nonlocal task
        task = asyncio.create_task(watch_queue())

    @app.on_event("shutdown")
    async def shutdown_event():
        nonlocal task
        task.cancel()


async def watch_queue():
    import asyncio

    global QUEUE
    global COMPLTED

    while True:
        while QUEUE:
            cmd = QUEUE.pop(0)
            print("[RUN START]!!!!!!!")
            result = run_shell(cmd)
            print("[RUN END]!!!!!!!")
            COMPLTED.append(result)
        await asyncio.sleep(30)
        print("[WAIT RUN]!!!!!!!")


def run_shell(cmd):
    with subprocess.Popen(
        cmd, encoding="UTF-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE
    ) as p:
        success = []
        errors = []
        for line in p.stdout:
            success.append(line)
        p.wait()
        for line in p.stderr:
            errors.append(line)
        print(f"return: {p.returncode}")
        if p.returncode:
            result = "".join(success) + "\n" + "".join(errors)
        else:
            result = "".join(success)

        return {"returncode": p.returncode, "result": result}
