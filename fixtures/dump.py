import json

import app.session


class DumpData:
    """Класс, позволяющий загрузить данные из json файла в бд"""

    def __init__(self, file_path: str = "../fixtures/data.json"):
        self.__file_path = file_path
        self.__metadata = app.session.Metadata
        self.__engine = app.session.engine

    def __load_data_from_file(self) -> dict:
        """Функция преобразует данные из файла в словарь"""
        with open(self.__file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def load_data_to_db(self) -> bool:
        """Функция загружает данные из словаря в бд"""
        fixtures = self.__load_data_from_file()
        with self.__engine.connect() as connection:
            for table_name, table_data in fixtures.items():
                table = self.__metadata.tables[table_name]
                for row_data in table_data:
                    insert_statement = table.insert().values(row_data)
                    connection.execute(insert_statement)
                connection.commit()
        return True


dumping = DumpData()
if dumping.load_data_to_db():
    print("Данные из файла успешно загружены в бд")
