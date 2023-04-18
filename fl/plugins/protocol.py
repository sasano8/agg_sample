

class SequentialProtocol:
    ENUM_SEVER = 0
    ENUM_CLIENT = 1

    def __init__(self, mode: int, comm, context):
        self.comm = comm
        self.context = context
        
        if mode == 0:
            self.state = self.SERVER.copy()
        elif mode == 1:
            self.state = self.CLIENT.copy()
        else:
            raise Exception()

    CLIENT = [
        "send_connect",
        "send_request_global_meta",
        "send_request_global_model",
        "send_model_meta",
        "send_model_file",
        "send_aggregation",
        "send_disconnect"
    ]
    
    SERVER = [
        "recv_connect",
        "recv_request_global_meta",
        "recv_request_global_model",
        "recv_model_meta",
        "recv_model_file",
        "recv_aggregation",
        "recv_disconnect"
    ]
    
    def on_send(self, body, event_name, **kwargs):
        kwargs["event_name"] = event_name
        func = getattr(self, event_name)
        result = func(body, **kwargs)
        return result
        
    def on_recive(self, body, event_name, **kwargs):
        kwargs["event_name"] = event_name
        func = getattr(self, event_name)
        result = func(body, **kwargs)
        return result
        
    def send_connect(self):
        ...

    def recv_connect(self):
        ...
        
    def send_request_global_meta(self):
        ...

    def recv_request_global_meta(self):
        ...

    def send_request_global_model(self):
        ...

    def recv_request_global_model(self):
        ...

    def send_model_meta(self):
        ...
        
        
    def recv_model_file(self):
        ...


    def send_model_file(self):
        ...
        
        
    def recv_model_file(self):
        ...


    def send_aggregation(self):
        ...
        
        
    def recv_aggregation(self):
        ...


    def send_disconnect(self):
        ...
        
        
    def recv_disconnect(self):
        ...


class P2PProtocol:
    ...
