from . import state


def add_handler(app):
    @app.on_event("startup")
    async def startup_event():
        state.__enter__()

    @app.on_event("shutdown")
    async def shutdown_event():
        state.__exit__()
