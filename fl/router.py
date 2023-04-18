from functools import wraps

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from .store import InmemoryStore
from .exceptions import RFC7807Error
from .core import V1Object

router = APIRouter()


# 永続化できるキーバリューストアが必要
# 有効期限管理はオブジェクトストレージに任せる
file_store = InmemoryStore()
state_store = InmemoryStore()
PLUGINS_URL = ""

client = V1Object(file_store=file_store, state_store=state_store, modules=PLUGINS_URL)


def handle_exc(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func()
        except RFC7807Error as e:
            return e.to_response()
        except Exception:
            raise

    return wrapper


@router.post("/v1/rpc/configurate")
@handle_exc
def configurate(config: dict):
    token = {}
    ret = client.configurate(config)
    return ret


@router.get("/v1/websocket/join")
@handle_exc
def subscribe(id: str):
    return client.subscribe(id)


@router.post("/v1/rpc/join")
@handle_exc
def join():
    token = {}
    ret = client.join()
    return ret


@router.post("/v1/rpc/connect")
@handle_exc
def connect():
    token = {}
    ret = client.connect()
    return ret


@router.post("/v1/rpc/disconnect")
@handle_exc
def disconnect():
    token = {}
    ret = client.disconnect()
    return ret


@router.post("/v1/rpc/get_federation")
@handle_exc
def get_federation_info(id: str):
    return client.get_federation_info(id)


@router.post("/v1/rpc/send_file")
@handle_exc
def send_file(id: str, token: str):
    return client.send_file(id, token)


@router.post("/v1/rpc/load_file")
@handle_exc
def load_file(id: str, token: str):
    def generate(file_path):
        with client.load_file(id, token) as file_like:
            yield from file_like

    return StreamingResponse(
        generate("filepath"), media_type="application/octet-stream"
    )


@router.post("/v1/rpc/aggregate")
@handle_exc
def aggregate(id: str, artifact):
    return client.request_aggregate(id, artifact)


@router.get("/v1/spec/formats")
@handle_exc
def list_format():
    return client.list_format()


@router.get("/v1/spec/formats/{name}")
@handle_exc
def get_format(name: str):
    return client.get_format(name)


@router.get("/v1/spec/structures")
@handle_exc
def list_structure():
    return client.list_stracture()


@router.get("/v1/spec/structures/{name}")
@handle_exc
def get_stracture(name: str):
    return client.get_stracture(name)


@router.get("/v1/spec/serializers")
@handle_exc
def list_serializer():
    return client.list_serializer()


@router.get("/v1/spec/serializers/{name}")
@handle_exc
def get_serializer(name: str):
    return client.get_serializer()


@router.get("/v1/spec/deserializers")
@handle_exc
def list_deserializer():
    return client.list_deserializer()


@router.get("/v1/spec/deserializers/{name}")
@handle_exc
def get_deserializer(name: str):
    return client.get_deserializer(name)


@router.get("/v1/spec/aggragators")
@handle_exc
def list_aggragator():
    return client.list_aggragator()


@router.get("/v1/spec/aggragators/{name}")
@handle_exc
def get_aggragator(name: str):
    return client.get_aggragator(name)


@router.get("/v1/spec/communicators")
@handle_exc
def list_communicator():
    return client.list_communicator()


@router.get("/v1/spec/communicators/{name}")
@handle_exc
def get_communicator(name: str):
    return client.get_communicator()


@router.get("/v1/spec/protocols")
@handle_exc
def list_protocol():
    return client.list_protocol()


@router.get("/v1/spec/protocols/{name}")
@handle_exc
def get_protocol(name: str):
    return client.get_protocol(name)


@router.get("/v1/spec/compressors")
@handle_exc
def list_compressor():
    return client.list_compressor()


@router.get("/v1/spec/compressors/{name}")
@handle_exc
def get_compressor(name: str):
    return client.get_compressor(name)


@router.get("/v1/spec/decompressors")
@handle_exc
def list_decompressor():
    return client.list_decompressor()


@router.get("/v1/spec/decompressors/{name}")
@handle_exc
def get_decompressor(name: str):
    return client.get_decompressor(name)


@router.get("/v1/spec/stores")
@handle_exc
def list_store():
    return client.list_store()


@router.get("/v1/spec/stores/{name}")
@handle_exc
def get_store(name: str):
    return client.get_store()
