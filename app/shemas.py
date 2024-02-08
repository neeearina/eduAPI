import pydantic


class ClubBase(pydantic.BaseModel):
    id: int
    name: str


class Club(ClubBase):
    description: str
    city_id: int
    organization_id: int

    # class Config:
    #     orm_mode = True


class CreateClub(pydantic.BaseModel):
    name: str
    description: str
    city_id: int
    organization_id: int
