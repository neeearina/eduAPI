import typing

import fastapi

import session
import shemas

router = fastapi.APIRouter(
    prefix="/clubs",
    tags=["Clubs", "Cities"],
)


@router.get("/", response_model=typing.List[shemas.ClubBase])
def get_all_clubs():
    """Получить все кружки, которые есть"""
    with session.Session() as my_session:
        return my_session.query(session.Clubs.id, session.Clubs.name).all()


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED,
             response_model=shemas.Club)
def create_club(club_info: shemas.CreateClub):
    """Создать новый кружок"""
    with session.Session() as my_session:
        new_club = session.Clubs(**club_info.dict())
        is_city = (
            my_session.query(session.Cities)
            .filter_by(id=club_info.city_id).first()
        )
        if not is_city:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no city with id: {club_info.city_id}",
            )
        is_org = (
            my_session.query(session.Organizations)
            .filter_by(id=club_info.organization_id).first()
        )
        if not is_org:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no organization with id: {club_info.city_id}",
            )
        my_session.commit()
        return (
            my_session.query(session.Clubs)
            .filter_by(id=new_club.id).first()
        )


@router.get("/city/{city_id}", response_model=typing.List[shemas.ClubBase])
def get_clubs_by_cities(city_id: int):
    """Получить все кружки, которые существуют в определенном городе"""
    with session.Session() as my_session:
        is_city = (
            my_session.query(session.Cities)
            .filter_by(id=city_id).first()
        )
        if not is_city:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"city with id: {city_id} was not found",
            )
        clubs_by_city = (
            my_session.query(session.Clubs.id, session.Clubs.name)
            .filter_by(city_id=city_id).all()
        )
        if not clubs_by_city:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no clubs in city with id: {city_id}",
            )
        return clubs_by_city
