import faker
import typing

import session


class FakeData:
    """Класс, методы которого создают фейковые данные в определенных таблицах"""

    def __init__(self, region: str = "ru_RU"):
        self.__faker = faker.Faker(region)
        self.__session = session.Session()

    def create_city(self, quantity: int = 5) -> None:
        for _ in range(quantity):
            city_obj = session.Cities(
                name=self.__faker.city()
            )
            self.__session.add(city_obj)
            self.__session.commit()

    def create_tags(self, quantity: int = 6, tags_lst: typing.Optional[list] = None,
                    description_lst: typing.Optional[list] = None) -> None:
        if ((tags_lst is None or description_lst is None) or
                ((tags_lst is not None and description_lst is not None) and
                 (len(tags_lst) == 0 or len(description_lst) == 0) or
                 len(tags_lst) != len(description_lst))):
            tags_lst = [self.__faker.sentence(nb_words=1) for _ in range(quantity)]
            description_lst = [self.__faker.sentence(nb_words=10) for _ in range(quantity)]

        for i in range(len(tags_lst)):
            tag_obj = session.Tags(
                name=tags_lst[i],
                description=description_lst[i],
            )
            self.__session.add(tag_obj)
            self.__session.commit()

    def close_session(self):
        self.__session.close()


# данные для заполнения таблицы еags
tags = ["Математика", "Логика", "Проектное"]
descriptions = ["Математика азвивает алгоритмическое мышление",
                "Логика учит концентрироваться, развивает память",
                "Проектная деятельность позволяет вовлекать детей в науку"]
if __name__ == "__main__":
    my_fake_data = FakeData()
    my_fake_data.create_city()
    my_fake_data.create_tags()
    my_fake_data.close_session()
