import typing

import fastapi

import session
import shemas

router = fastapi.APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.get("/", response_model=typing.List[shemas.Organization])
def get_all_org(limit: int = 10):
    """Получить все организации"""
    with session.Session() as my_session:
        return (
            my_session.query(session.Organizations).limit(limit).all()
        )


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED,
             response_model=shemas.OrganizationOut)
def create_org(org_info: shemas.OrganizationBase):
    """Создать организацию"""
    with session.Session() as my_session:
        new_org = session.Organizations(**org_info.dict())
        my_session.add(new_org)
        my_session.commit()
        return (
            my_session.query(session.Organizations)
            .filter_by(id=new_org.id).first()
        )


@router.get("/{org_id}", response_model=shemas.OrganizationOut)
def get_org_by_id(org_id: int):
    """Получить оргиназвцию по id"""
    with session.Session() as my_session:
        org = (
            my_session.query(session.Organizations)
            .filter_by(id=org_id).first()
        )
        if not org:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no organization with id: {org_id}",
            )
        return org


@router.put("/{org_id}", response_model=shemas.OrganizationOut)
def put_org_by_id(org_id: int, update_org_info: shemas.OrganizationBase):
    """Изменить организацию по id"""
    with session.Session() as my_session:
        org_query = (
            my_session.query(session.Organizations)
            .filter_by(id=org_id)
        )
        org = org_query.first()
        if not org:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"organization with id: {org_id} was not found",
            )
        org_query.update(update_org_info.dict(), synchronize_session=False)
        my_session.commit()
        return org_query.first()


@router.delete("/{org_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete_org(org_id: int):
    with session.Session() as my_session:
        org_query = (
            my_session.query(session.Organizations)
            .filter_by(id=org_id)
        )
        org = org_query.first()
        if not org:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"organization with id: {org_id} was not found",
            )
        org_query.delete(synchronize_session=False)
        my_session.commit()
        return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)
