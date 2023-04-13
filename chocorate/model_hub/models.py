from sqlmodel import SQLModel, Field


class Hub(SQLModel, table=True):
    id: int = Field(primary_key=True)
    description: str = ""
    host: str = "asdfasdfasdfasdfasdfas"
    params: dict = {}

    def discriminate(self):
        if 1:
            return HanggingFace()
        elif 2:
            return MLFlow()
        elif 3:
            return XData()
        else:
            raise Exception()

    def inspect(self):
        ...


class HanggingFace:
    ...


class MLFlow:
    ...


class XData:
    ...
