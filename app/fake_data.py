import faker

import session


class FakeData:
    """Класс, методы которого создают фейковые данные в таблицах"""

    def __init__(self, region: str = "ru_RU", quantity: int = 5):
        self._quantity = quantity
        self.__faker = faker.Faker(region)
        self.__session = session.Session()

    def create_data(self) -> None:
        """Главный метод, вызывающий по порядку функции для заполнения таблиц.
        Порядок  вызова функции лучше не изменять"""
        self.__create_city()
        self.__create_tags()
        self.__create_organizations()
        self.__create_clubs()
        self.__create_clubs_and_tags()
        self.__close_session()

    def __create_city(self) -> None:
        for _ in range(self._quantity):
            city_obj = session.Cities(
                name=self.__faker.city(),
            )
            self.__session.add(city_obj)
            self.__session.commit()

    def __create_tags(self) -> None:
        tags_lst = [
            self.__faker.sentence(nb_words=1) for _ in range(self._quantity)
        ]

        description_lst = [
            self.__faker.sentence(nb_words=10) for _ in range(self._quantity)
        ]
        for i in range(self._quantity):
            tag_obj = session.Tags(
                name=tags_lst[i],
                description=description_lst[i],
            )
            self.__session.add(tag_obj)
            self.__session.commit()

    def __create_organizations(self):
        for _ in range(self._quantity):
            organization_obj = session.Organizations(
                name=self.__faker.company(),
                director=self.__faker.name(),
                email=self.__faker.ascii_company_email(),
                site=self.__faker.url(),
                address=self.__faker.address(),
            )
            self.__session.add(organization_obj)
            self.__session.commit()

    def __create_clubs(self):
        for i in range(self._quantity):
            city_obj = (
                self.__session.query(session.Cities)
                .filter_by(id=i + 1).first()
            )
            organization_obj = (
                self.__session.query(session.Organizations).
                filter_by(id=i + 1).first()
            )
            club_obj = session.Clubs(
                name=self.__faker.company(),
                description=self.__faker.sentence(nb_words=10),
                city_id=city_obj.id,
                organization_id=organization_obj.id,
            )
            self.__session.add(club_obj)
            self.__session.commit()

    def __create_clubs_and_tags(self):
        for i in range(self._quantity):
            club_obj = (
                self.__session.query(session.Clubs)
                .filter_by(id=i + 1).first()
            )
            tag_obj = (
                self.__session.query(session.Tags)
                .filter_by(id=i + 1).first()
            )
            obj = session.ClubsTags(
                club_id=club_obj.id,
                tag_id=tag_obj.id,
            )
            self.__session.add(obj)
            self.__session.commit()

    def __close_session(self):
        self.__session.close()


if __name__ == "__main__":
    my_fake_data = FakeData()
    my_fake_data.create_data()
