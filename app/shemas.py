import datetime

import pydantic


class ClubBase(pydantic.BaseModel):
    id: int
    name: str


class ClubOut(ClubBase):
    description: str
    city_id: int
    organization_id: int


class CreateClub(pydantic.BaseModel):
    name: str
    description: str
    city_id: int
    organization_id: int


class OrganizationBase(pydantic.BaseModel):
    name: str
    director: str
    email: str
    site: str
    address: str


class OrganizationGet(pydantic.BaseModel):
    id: int
    name: str


class OrganizationOut(OrganizationBase):
    id: int


class TagBase(pydantic.BaseModel):
    name: str
    description: str


class TagOut(TagBase):
    id: int


class UserCreate(pydantic.BaseModel):
    email: pydantic.EmailStr
    password: str


class UserOut(pydantic.BaseModel):
    id: int
    email: pydantic.EmailStr
    created_at: datetime.datetime
