import typing

import fastapi
import sqlalchemy

import session
import shemas
import utils

router = fastapi.APIRouter(
    prefix="/clubs",
    tags=["Clubs", "Cities"],
)


@router.get("/", response_model=typing.List[shemas.ClubBase])
def get_all_clubs(limit: int = 10):
    """Получить все кружки"""
    with session.Session() as my_session:
        clubs = (
            my_session.query(session.Clubs.id, session.Clubs.name)
            .limit(limit).all()
        )
        if not clubs:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="no clubs",
            )
        return clubs


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED,
             response_model=shemas.ClubOut)
def create_club(club_info: shemas.CreateClub):
    """Создать кружок"""
    with session.Session() as my_session:
        new_club = session.Clubs(**club_info.dict())
        if not utils.check_is_exist(session.Cities, club_info.city_id):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no city with id: {club_info.city_id}",
            )
        if not utils.check_is_exist(session.Organizations,
                                    club_info.organization_id):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no organization with id: {club_info.city_id}",
            )
        my_session.add(new_club)
        my_session.commit()
        return (
            my_session.query(session.Clubs)
            .filter_by(id=new_club.id).first()
        )


@router.get("/{club_id}", response_model=shemas.ClubOut)
def get_club_by_id(club_id: int):
    """Получить определенный кружок"""
    with session.Session() as my_session:
        club = my_session.query(session.Clubs).filter_by(id=club_id).first()
        if not club:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no city with id: {club_id}",
            )
        return club


@router.put("/{club_id}", response_model=shemas.ClubOut)
def put_club_by_id(club_id: int, update_club_info: shemas.CreateClub):
    """Изменить определенный кружок"""
    with session.Session() as my_session:
        club_query = my_session.query(session.Clubs).filter_by(id=club_id)
        club = club_query.first()
        if not club:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no club with id: {club_id}",
            )
        club_query.update(update_club_info.dict(), synchronize_session=False)
        my_session.commit()
        return club_query.first()


@router.delete("/{club_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete_club_by_id(club_id: int):
    """Удалить определенный кружок"""
    with session.Session() as my_session:
        club_query = my_session.query(session.Clubs).filter_by(id=club_id)
        club = club_query.first()
        if not club:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no club with id: {club_id}",
            )
        club_query.delete(synchronize_session=False)
        my_session.commit()
        return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@router.get("/city/{city_id}", response_model=typing.List[shemas.ClubBase])
def get_clubs_by_cities(city_id: int, tags: typing.List = fastapi.Query(),
                        limit: int = 10):
    """Получить все кружки, которые существуют в определенном городе
     по тегам"""
    with session.Session() as my_session:
        if not utils.check_is_exist(session.Cities, city_id):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no city with id: {city_id}",
            )
        filters = [session.Tags.name == v for v in tags]
        tags_lst = (
            my_session.query(session.Tags.id)
            .filter(sqlalchemy.or_(*filters)).all()
        )
        if not tags_lst:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="no tags with such names",
            )
        filters = [session.ClubsTags.tag_id == v[0] for v in tags_lst]
        clubs_by_tags = (
            my_session.query(session.ClubsTags.club_id)
            .filter(sqlalchemy.or_(*filters))
        )
        unique_clubs_id = set(v[0] for v in clubs_by_tags)
        filters = [
            session.Clubs.id == v and session.Clubs.city_id == city_id
            for v in unique_clubs_id
        ]
        clubs_by_city = (
            my_session.query(session.Clubs.id, session.Clubs.name)
            .filter(sqlalchemy.or_(*filters)).limit(limit).all()
        )
        if not clubs_by_city:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no clubs in city with id: {city_id}",
            )
        return clubs_by_city
