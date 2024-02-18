import fastapi

import session
import shemas
import utils

router = fastapi.APIRouter(
    tags=["Authentication"],
)


@router.post("/loggin")
def login(user_credentials: shemas.User):
    with session.Session() as my_session:
        user = (
            my_session.query(session.User)
            .filter_by(email=user_credentials.email).first()
        )
        if (not user or
                not utils.verify(user_credentials.password, user.password)):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="invalid credentials",
            )
        return {"token": "example token"}
