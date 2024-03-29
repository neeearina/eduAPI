import fastapi

import session
import shemas
import utils

router = fastapi.APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", status_code=fastapi.status.HTTP_201_CREATED,
             response_model=shemas.UserOut)
def create_user(user_info: shemas.User):
    """Создать пользователя"""
    with session.Session() as my_session:
        hashed_password = utils.hash(user_info.password)
        user_info.password = hashed_password
        new_user = session.User(**user_info.dict())
        my_session.add(new_user)
        my_session.commit()
        return (my_session.query(session.User)
                .filter_by(id=new_user.id).first())


@router.get("/{user_id}", response_model=shemas.UserOut)
def get_user(user_id: int):
    """Получить пользователя"""
    with session.Session() as my_session:
        user = (
            my_session.query(session.User)
            .filter_by(id=user_id).first()
        )
        if not user:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_403_FORBIDDEN,
                detail=f"no user with id: {user_id}",
            )
        return user
