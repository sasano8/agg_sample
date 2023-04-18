import json
from fastapi.responses import JSONResponse


class RFC7807Error(Exception):
    def __init__(self, status_code, title, detail, headers: dict = {}):
        data = {
            "status_code": status_code,
            "title": title,
            "detail": detail,
            "headers": headers,
            # "fields": fields,
        }
        
        super().__init__(data)

    @property
    def data(self) -> dict:
        return self.args[0]

    @property
    def json(self):
        return json.dumps(self.args[0])

    def to_dict(self):
        return self.data

    def to_response(self):
        content = self.data
        return JSONResponse(
            content,
            status_code=self.status_code,
            media_type="application/problem+json",
            headers=self.headers,
        )
