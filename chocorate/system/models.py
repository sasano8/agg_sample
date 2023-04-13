from sqlmodel import SQLModel, Field


class System(SQLModel, table=True):
    id: int = Field(primary_key=True)
    is_maintenance: bool = False
