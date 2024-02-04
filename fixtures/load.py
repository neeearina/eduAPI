import json

import app.session


class LoadData:
    """Класс, создающий фикстуры в json формате из данных в бд"""

    def __init__(self, file_path: str = "../fixtures/data.json"):
        self.__file_path = file_path
        self.__all_data = {}
        self.__my_session = app.session.Session()

    def create_data_for_file(self) -> bool:
        """Функция преобразует данные из таблиц в словарь"""
        for table in app.session.Metadata.sorted_tables:
            table_data = []
            for row in self.__my_session.query(table).all():
                table_data.append({
                    col.name: getattr(row, col.name) for col in table.columns
                })
            self.__all_data[table.name] = table_data
        self.__my_session.close()
        return self.__load_data_in_file()

    def __load_data_in_file(self) -> bool:
        """Функция записывает преобразованные данные в json файл"""
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(self.__all_data, file, ensure_ascii=False, indent=2)
        return True


loading = LoadData()
if loading.create_data_for_file():
    print("Данные из бд успешно загружены в json файл")
