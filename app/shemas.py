import pydantic


class ClubsByCity(pydantic.BaseModel):
    id: int
    name: str
