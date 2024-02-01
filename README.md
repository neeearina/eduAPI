# tyumeneduAPI

API c информацией о кружках и занятиях в городе Тюмени

# БД с таблицей

https://dbdiagram.io/d/eduAPI-65b0f548ac844320ae9e6953

---

# Работа с alembic

### Установить и инициализировать

```commandline
pip install alembic
```

```commandline
alembic init migrations
```

#### После инициализации будет создана директория *migrations* (с файлами *readme*, *env.py*, *script.py.mako*).

#### В директории, где выполнялся скрипт появляется файл *alembic.ini*.

### Настройка

* В файле *alembic.ini* настроить *sqlalchemy.url* - указать путь до базы данных.

* В файле *env.py* yастроить переменную *target_metadata*, в которую передается базовый класс для моделей-таблиц.

* Импорты классов таблиц-моделей лучше сделать в файл *__init__* в том же пакете, где объявлен базовый класс.

### Первая миграция

```commandline
alembic revision --autogenerate -m 'initial'
```

*initial* - название первой миграции

### Применить миграцию

```commandline
alembic upgrade 4be659b1e34b
```

*4be659b1e34b* - хеш миграции
