class V1Object:
    def __init__(self, file_store, state_store, modules, upstream_store):
        self.file_store = file_store
        self.state_store = state_store
        self.modules = modules

    def add_upstream(self, **kwargs):
        ...

    def configurate(self, config: dict):
        token = {}
        return token

    def join(self):
        return token

    def connect(self):
        return token

    def disconnect(self):
        return token

    def get_federation_info(self, id: str):
        return self.file_store.load_json(id)

    def request_aggregate(id: str, artifact):
        # tar.gz tarはまとめる gzipは圧縮

        conf = file_store[id]
        deserializer = conf.get_deserializer()
        aggregate = conf.get_algorithm()
        path = artifact.get_path("model")
        # readonley = fsspec(path)
        model = deserialize(path)
        objects = aggregate(model, meta)
        return object_paths

    def subscribe(self, id: str):
        raise NotImplementedError()

    def send_file(id: str, token: str):
        ...

    def load_file(self, id: str):
        f = open(id, mode="rb")
        return f

    def list_stracture(self):
        return self.modules["stracture"]

    def get_stracture(self, name):
        return self.modules["stracture"][name]

    def list_format(self):
        return self.modules["format"]
        # return [{"name": "safetensor"}]

    def get_format(self, name: str):
        return self.modules["format"][name]

    def list_serializer(self):
        return self.modules["serializer"]

    def get_serializer(self, name: str):
        return self.modules["serializer"][name]

    def list_deserializer(self):
        return self.modules["deserializer"]

    def get_deserializer(self, name: str):
        return self.modules["deserializer"][name]

    def list_aggragator(self):
        return self.modules["aggragator"]

    def get_aggragator(self, name: str):
        return self.modules["aggragator"][name]

    def list_communicator(self):
        return self.modules["communicator"]

    def get_communicator(self, name: str):
        return self.modules["communicator"][name]

    def list_protocol(self):
        return self.modules["protocol"]

    def get_protocol(self, name: str):
        return self.modules["protocol"][name]

    def list_compressor(self):
        return self.modules["compressor"]

    def get_compressor(self, name: str):
        return self.modules["compressor"][name]

    def list_decompressor(self):
        return self.modules["decompressor"]

    def get_decompressor(self, name: str):
        return self.modules["decompressor"][name]

    def list_store(self):
        return self.modules["store"]

    def get_store(self, name: str):
        return self.modules["store"][name]
