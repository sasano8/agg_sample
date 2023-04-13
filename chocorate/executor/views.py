from sqlmodel import SQLModel, Field, Session, create_engine
from sqlalchemy import select, text
from typing import Union
from sqladmin import ModelView


class Indexer:
    def __call__(self, id: int, mode: str = "test", global_or_local: str = "local"):
        pass


DEFAULT_GIT_HOST = "https://github.com"
DEFAULT_EXECUTOR = ""


class ConfigTenant(SQLModel, table=True):
    id: int = Field(primary_key=True)
    uuid: str = "asdfasdfasdfasdfasdfas"
    name: str
    description: str = ""


class ConfigUpstream(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str = ""
    url: str


class ConfigAggregator(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str = ""
    upstream: int = None
    dir: str = DEFAULT_GIT_HOST
    only_trusted_party: bool = True
    add_party: bool = False
    is_system: bool = True
    next_state: str = "init"
    stopped: bool = False

    def get_default_client_config(self):
        # stable ai のパクリ
        return {
            "agg_host": "<ここにIPアドレスを書き込む>",
            "seed": None,
            "token": "asdfasdfa",
            "client_name": "aaaa",
        }

    def get_clients(self):
        return []

    def index_files(self, indexer: Indexer):
        for model in range(1):
            indexer(model)

    def inspect(self):
        "モデルを自動的に解析する"

    def query_most_recent_global(self):
        ...

    def query_best_performance_global(self):
        ...

    def query_most_recent_local(self):
        ...

    def query_best_performance_local(self):
        ...

    def serve(self):
        ...


class ConfigExperiment(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str = ""
    upstream: int = None
    agg_config: int
    dir: str = DEFAULT_GIT_HOST
    is_editable: bool = True  # システムデフォルトの値としてロックしたい場合に使用する

    def clone(self):
        """ローカルにgitリポジトリをクローンする"""
        ...


class ConfigExecutorProfile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    description: str = ""
    upstream: int = None
    num: int = 1
    cpu_or_gpu: str = "cpu"
    no_proxy: str = "localhost"
    http_proxy: str = None
    https_proxy: str = None


class ConfigExecutor(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str = "k8s"  # shell


class Run(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str = "k8s"  # shell
    running: bool = False
    completed: bool = False
    command: str = ""


class ConfigTenantAdmin(ModelView, model=ConfigTenant):
    column_list = list(ConfigTenant.__fields__)


class ConfigAggregatorAdmin(ModelView, model=ConfigAggregator):
    column_list = list(ConfigAggregator.__fields__)


class ConfigExperimentAdmin(ModelView, model=ConfigExperiment):
    column_list = list(ConfigExperiment.__fields__)


class ConfigUpstreamAdmin(ModelView, model=ConfigUpstream):
    column_list = list(ConfigUpstream.__fields__)


class ConfigExecutorAdmin(ModelView, model=ConfigExecutor):
    column_list = list(ConfigExecutor.__fields__)


class ConfigExecutorProfileAdmin(ModelView, model=ConfigExecutorProfile):
    column_list = list(ConfigExecutorProfile.__fields__)


class RunAdmin(ModelView, model=Run):
    column_list = list(Run.__fields__)
