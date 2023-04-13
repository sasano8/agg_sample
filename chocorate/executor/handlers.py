import subprocess
from .models import Run
from sqlalchemy import select
from typing import cast
from time import sleep
import json
from asyncer import asyncify

from chocorate.abc.db import get_session
from chocorate.abc import state


def add_handler(app):
    import asyncio
    from asyncio import Task

    task: Task

    @app.on_event("startup")
    async def startup_event():
        nonlocal task
        awaitable = asyncify(watch_queue)(state)
        task = asyncio.create_task(awaitable)

    @app.on_event("shutdown")
    async def shutdown_event():
        nonlocal task
        task.cancel()


def watch_queue(token):
    # TODO: 例外発生時にどこにも情報が通達されないのでハンドラをかませること
    while token.active:
        try:
            with get_session() as session:
                stmt = select(Run).where(Run.started == False)
                for run in session.exec(stmt).scalars():
                    run = cast(Run, run)
                    print("[RUN START]!!!!!!!")

                    try:
                        print(run.command)
                    except Exception as e:
                        print(type(run))
                        print(e)
                    cmd = json.loads(run.command)
                    if not isinstance(cmd, list):
                        run.started = True
                        run.returncode = -1
                        run.completed = True
                        session.add(run)
                        session.commit()
                    else:
                        run.started = True
                        run.returncode = -1
                        run.completed = False
                        session.add(run)
                        session.commit()
                        
                        if run.entrypoint == "docker":
                            ...
                        elif run.entrypoint == "k8s":
                            "kubectl create job hello-world --image=hello-world"
                            "kubectl get jobs"
                            """
                            NAME         COMPLETIONS DURATION AGE
                            hello-world  1/1         5s       2ms
                            """
                            "kubectl delete jobs hello-world"
                        else:
                            raise Exception(f"Not supported entrypoint: {run.entrypoint}")

                        result = run_shell(run.entrypoint, *cmd)
                        run.started = True
                        run.completed = True
                        run.returncode = result["returncode"]
                        run.result = result["result"]
                        session.add(run)
                        session.commit()
                    print("[RUN END]!!!!!!!")

        except Exception as e:
            print(e)

        sleep(10)
        print("[WAIT RUN]!!!!!!!")


def run_shell(*args):
    with subprocess.Popen(
        args, encoding="UTF-8", stdout=subprocess.PIPE, stderr=subprocess.PIPE
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
