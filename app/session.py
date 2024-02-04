import re

import sqlalchemy.orm

DATABASE_NAME = "db.sqlite"

engine = sqlalchemy.create_engine(f"sqlite:///{DATABASE_NAME}")
Session = sqlalchemy.orm.sessionmaker(bind=engine)

Base = sqlalchemy.orm.declarative_base()
Metadata = sqlalchemy.MetaData()
Metadata.reflect(bind=engine)


def create_db():
    Base.metadata.create_all(engine)


class Cities(Base):
    """Класс, описывающий таблицу с названиями городов"""

    __tablename__ = "cities"

    id = sqlalchemy.Column(
        type_=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        doc="Уникальный идентификатор города",
    )
    name = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=False,
        unique=True,
        doc="Название города",
    )

    def __repr__(self):
        return self.name


class Clubs(Base):
    """Класс, описывающий таблицу с кружками и занятиями"""

    __tablename__ = "clubs"

    id = sqlalchemy.Column(
        type_=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        doc="Уникальный идентификатор кружка",
    )
    name = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=False,
        doc="Название кружка",
    )
    description = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=False,
        doc="Описание кружка",
    )
    city_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            column="cities.id",
            ondelete="CASCADE",
        ),
        type_=sqlalchemy.Integer,
        nullable=False,
        doc="Город, где располагается кружок",
    )
    organization_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey(
            column="organizations.id",
            ondelete="CASCADE",
        ),
        type_=sqlalchemy.Integer,
        nullable=False,
        doc="Организация, к которой относится кружок",
    )
    organization = sqlalchemy.orm.relationship("Organizations", backref="club")

    def __repr__(self):
        return self.name


class ClubsTags(Base):
    """Класс, описывающий отношение Many2Many для таблиц Clubs и Tags"""

    __tablename__ = "clubs_tags"

    id = sqlalchemy.Column(
        type_=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        doc="Уникальный идентификатор записи связи M2M между клубом и тегом",
    )

    club_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("clubs.id"),
        type_=sqlalchemy.Integer,
        doc="Уникальный индентификатор кружка",
    )
    tag_id = sqlalchemy.Column(
        sqlalchemy.ForeignKey("tags.id"),
        type_=sqlalchemy.Integer,
        doc="Уникальный индентификатор тега",
    )


class Organizations(Base):
    """Класс, описывающий таблицу организаций"""

    __tablename__ = "organizations"

    id = sqlalchemy.Column(
        type_=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        doc="Уникальный идентификатор организации",
    )
    name = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=False,
        unique=True,
        doc="Название организации",
    )
    director = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=False,
        doc="Управляющий",
    )
    email = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=True,
        unique=True,
        doc="Электронная почта",
    )
    site = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=True,
        unique=True,
        doc="Основной веб сайт организации",
    )
    address = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=True,
        doc="Адрес",
    )

    @sqlalchemy.orm.validates("email")
    def validate_email(self, key, mail: str):
        assert "@" in mail, "Некорректный email"
        return re.sub(r"[,?!.]", "", mail).lower()

    @sqlalchemy.orm.validates("site")
    def validate_site(self, key, url: str):
        pattern = (
            r"https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\."
            r"[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)"
        )
        assert re.match(pattern, url), "Некорректный url"
        return url

    def __repr__(self):
        return self.name


class Tags(Base):
    """Класс, описывающий названия(теги) направлений для кружков"""

    __tablename__ = "tags"

    id = sqlalchemy.Column(
        type_=sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
        doc="Уникальный идентификатор тега",
    )
    name = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=False,
        unique=True,
        doc="Название тега",
    )
    description = sqlalchemy.Column(
        type_=sqlalchemy.String,
        nullable=True,
        doc="Описание тега",
    )

    def __repr__(self):
        return self.name
