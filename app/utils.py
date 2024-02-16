import session


def check_is_exist(query_class, object_id):
    with session.Session() as my_session:
        is_exist = (
            my_session.query(query_class)
            .filter_by(id=object_id).first()
        )
        if is_exist:
            return True
        return False
