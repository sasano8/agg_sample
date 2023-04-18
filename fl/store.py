from typing import Dict
from io import BytesIO, StringIO
import json
import warnings


class IStore:
    def dump_json(self, key: str, obj):
        raise NotImplementedError()

    def load_json(self, key: str):
        raise NotImplementedError()

    def dump_bytes(self, key: str, obj):
        raise NotImplementedError()

    def load_bytes(self, key: str):
        raise NotImplementedError()

    def dump_text(self, key: str, obj):
        raise NotImplementedError()

    def load_text(self, key):
        raise NotImplementedError()


class InmemoryStore(IStore):
    def __init__(self):
        self.store: Dict[str, bytes] = {}
        warnings.warn(
            "InmemoryStore is not persistent and doesn't work properly in multiprocess environment. And Use it for testing only."
        )

    def dump_json(self, key: str, obj):
        encoded_data = json.dumps(obj).encode("utf-8")
        self.store[key] = encoded_data

    def load_json(self, key: str):
        return json.load(self.load_bytes(key))

    def dump_bytes(self, key: str, obj):
        self.store[key] = BytesIO(obj).getvalue()

    def load_bytes(self, key: str):
        obj = self.store[key]
        return BytesIO(obj)

    def dump_text(self, key: str, obj):
        self.store[key] = obj.encode("utf-8")

    def load_text(self, key):
        obj = self.store[key].decode("utf-8")
        return StringIO(obj)


class RedisStore(IStore):
    ...


class PostgresqlStore(IStore):
    ...
