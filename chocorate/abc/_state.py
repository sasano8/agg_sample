class AppState:
    def __init__(self):
        self.active = False

    def __enter__(self):
        self.active = True

    def __exit__(self, *args, **kwargs):
        self.active = False
