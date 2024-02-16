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


class OrganizationBase(pydantic.BaseModel):
    name: str
    director: str
    email: str
    site: str
    address: str


class Organization(pydantic.BaseModel):
    id: int
    name: str


class OrganizationOut(Organization, OrganizationBase):
    pass
