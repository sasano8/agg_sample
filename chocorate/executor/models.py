from sqlmodel import SQLModel, Field


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


class ConfigParty(SQLModel, table=True):
    id: int = Field(primary_key=True)
    agg_config: int
    name: str
    description: str = ""


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
    entrypoint: str = "docker"  # Literal["docker", "k8s", "shell"]
    command: str = '["run", "--rm", "hello-world"]'
    started: bool = False
    completed: bool = False
    returncode: int = -1
    result: str = ""
