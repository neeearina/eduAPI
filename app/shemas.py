import pydantic


class ClubBase(pydantic.BaseModel):
    id: int
    name: str


class Club(ClubBase):
    description: str
    city_id: int
    organization_id: int


class CreateClub(pydantic.BaseModel):
    name: str
    description: str
    city_id: int
    organization_id: int


class TagBase(pydantic.BaseModel):
    name: str
    description: str


class Tag(TagBase):
    id: int
