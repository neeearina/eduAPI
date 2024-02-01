import os

import session

if __name__ == "__main__":
    if not os.path.exists(session.DATABASE_NAME):
        session.create_db()
