import typing

import fastapi

import session
import shemas

router = fastapi.APIRouter(
    prefix="/clubs",
    tags=["Clubs", "Cities"],
)


def check_is_exist(query_class, object_id):
    with session.Session() as my_session:
        is_exist = (
            my_session.query(query_class)
            .filter_by(id=object_id).first()
        )
        if is_exist:
            return True
        return False


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
        if not check_is_exist(session.Cities, club_info.city_id):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no city with id: {club_info.city_id}",
            )
        if not check_is_exist(session.Organizations,
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


@router.get("/{club_id}", response_model=shemas.Club)
def get_club_by_id(club_id: int):
    """Получить определенный кружок по его id"""
    with session.Session() as my_session:
        club = my_session.query(session.Clubs).filter_by(id=club_id).first()
        if not club:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"club with id: {club_id} was not found",
            )
        return club


@router.put("/{club_id}", response_model=shemas.Club)
def put_club_by_id(club_id: int, update_club_info: shemas.CreateClub):
    """Изменить кружок по его id"""
    with session.Session() as my_session:
        club_query = my_session.query(session.Clubs).filter_by(id=club_id)
        club = club_query.first()
        if not club:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"club with id: {club_id} was not found",
            )
        club_query.update(update_club_info.dict(), synchronize_session=False)
        my_session.commit()
        return club_query.first()


@router.delete("/{club_id}", status_code=fastapi.status.HTTP_204_NO_CONTENT)
def delete_club(club_id: int):
    """Удалить кружок по его id"""
    with session.Session() as my_session:
        club_query = my_session.query(session.Clubs).filter_by(id=club_id)
        club = club_query.first()
        if not club:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"club with id: {club_id} was not found",
            )
        club_query.delete(synchronize_session=False)
        my_session.commit()
        return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@router.get("/city/{city_id}", response_model=typing.List[shemas.ClubBase])
def get_clubs_by_cities(city_id: int):
    """Получить все кружки, которые существуют в определенном городе"""
    with session.Session() as my_session:
        if not check_is_exist(session.Cities, city_id):
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
