import typing

import fastapi

import session
import shemas

router = fastapi.APIRouter(
    prefix="/clubs",
    tags=["Clubs"],
)


@router.get("/city/{city_id}", response_model=typing.List[shemas.ClubsByCity])
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
            my_session.query(session.Clubs)
            .filter_by(city_id=city_id).all()
        )
        if not clubs_by_city:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail=f"no clubs in city with id: {city_id}",
            )
        return clubs_by_city
