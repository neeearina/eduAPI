import passlib.context

import session

pwd_context = passlib.context.CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def check_is_exist(query_class, object_id):
    with session.Session() as my_session:
        is_exist = (
            my_session.query(query_class)
            .filter_by(id=object_id).first()
        )
        if is_exist:
            return True
        return False
