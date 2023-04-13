from sqlmodel import create_engine
from fastapi import FastAPI
from sqladmin import Admin as RootView
from chocorate.abc import db


def depend(*args, **kwargs):
    def wrapper(func):
        func(*args, **kwargs)
        return func

    return wrapper


def make_engine():
    engine = create_engine(
        "sqlite:///example.db",
        connect_args={"check_same_thread": False},
    )
    return engine


def create_admin_view(engine):
    from sqladmin import Admin
    from chocorate.auth.views import authentication_backend

    admin_view = Admin(
        app, engine, title="Chocorate", authentication_backend=authentication_backend
    )
    return admin_view


def setup_routers(app: FastAPI):
    from chocorate.executor.router import ci_router, queue_router

    app.include_router(ci_router, prefix="/ci")
    app.include_router(queue_router, prefix="/tasks")


def setup_handlers(app: FastAPI):
    from chocorate.abc.handlers import add_handler as abc_handler
    from chocorate.executor.handlers import add_handler as executor_handler

    abc_handler(app)
    executor_handler(app)


def setup_views(app: FastAPI, admin: RootView):
    from chocorate.executor.views import (
        ConfigTenantAdmin,
        ConfigExecutorAdmin,
        ConfigExecutorProfileAdmin,
        ConfigUpstreamAdmin,
        ConfigAggregatorAdmin,
        ConfigPartyAdmin,
        ConfigExperimentAdmin,
        RunAdmin,
    )
    from chocorate.system.views import SystemAdmin

    admin.add_view(ConfigTenantAdmin)
    admin.add_view(ConfigExecutorAdmin)
    admin.add_view(ConfigExecutorProfileAdmin)
    admin.add_view(ConfigUpstreamAdmin)
    admin.add_view(ConfigAggregatorAdmin)
    admin.add_view(ConfigExperimentAdmin)
    admin.add_view(ConfigPartyAdmin)
    admin.add_view(RunAdmin)
    admin.add_view(SystemAdmin)


app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})
engine = db.get_default_engine()
admin_view = create_admin_view(engine)

setup_routers(app)
setup_handlers(app)
setup_views(app, admin_view)
db.create_all(engine)
