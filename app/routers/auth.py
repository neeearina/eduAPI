import fastapi
import fastapi.security.oauth2 as security

import oauth2
import session
import utils

router = fastapi.APIRouter(
    tags=["Authentication"],
)


@router.post("/login")
def login(user_credentials: security.OAuth2PasswordRequestForm
          = fastapi.Depends()):
    with session.Session() as my_session:
        user = (
            my_session.query(session.User)
            .filter_by(email=user_credentials.username).first()
        )
        if (not user or
                not utils.verify(user_credentials.password, user.password)):
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_404_NOT_FOUND,
                detail="invalid credentials",
            )
        return {
            "access_token": oauth2.create_access_token(
                data={"user_id": user.id},
            ),
            "token_type": "bearer",
        }
