# eduAPI - API c информацией о кружках и занятиях дополнительного образования

###### *Проект создан в учебных целях. Тесты я когда-нибудь допишу, правда.*

---

# Инструкция по запуску проекта

### Склонируйте репозиторий с помощью git команды:

```commandline
git clone https://github.com/neeearina/eduAPI.git
```

### Создайте виртуальное окружение и активируйте его:

```commandline
python3 -m venv venv 
```

```commandline
source venv/bin/activate 
```

### Установите зависимости проекта:

```commandline
pip install -r requirements.txt
```

### Переменные виртуального окружения

#### В текущей директории создайте файл .env и заполните соими данными по примеру файла .env_example

###### *SECRET_KEY* - секретный ключ для jwt токена

###### *ALGORITHM* - алгоритм для шифрования

###### *ACCESS_TOKEN_EXPIRE_MINUTES* - время действия токена

### Примените миграции для базы данных:

```commandline
alembic upgrade 153fb29cf9e4
```

#### Перейдите в директорию с базой данных:

```commandline
cd app
```

###### Должен появиться файл *db.sqlite*. [ERD базы данных](https://dbdiagram.io/d/eduAPI-65b0f548ac844320ae9e6953)

### Заполните БД фейковыми данными, запустив файл fake_data.py

### Запустите сервер командой и перейдите по ссылке в терминале:

```commandline
uvicorn main:app --reload
```

### Документация проекта находится по пути /docs

---

# Здесь просто заметки для меня, чтобы я ничего не забыла))

## Работа с alembic

### Установить и инициализировать

```commandline
pip install alembic
```

```commandline
alembic init migrations
```

###### После инициализации будет создана директория *migrations* (с файлами *readme*, *env.py*, *script.py.mako*).

#### В директории, где выполнялся скрипт появляется файл *alembic.ini*.

### Настройка

* В файле *alembic.ini* настроить *sqlalchemy.url* - указать путь до базы данных.

* В файле *env.py* настроить переменную *target_metadata*, в которую передается базовый класс для моделей-таблиц.

* Импорты классов таблиц-моделей лучше сделать в файл *__init__* в том же пакете, где объявлен базовый класс.

### Первая миграция

```commandline
alembic revision --autogenerate -m 'initial'
```

###### *initial* - название первой миграции

### Применить миграцию

```commandline
alembic upgrade 4be659b1e34b
```

###### *4be659b1e34b* - хеш миграции из комментария *Revision ID* в последнем файле в папке migrations/versions

#### После выполнения команды выше - создаются таблицы в бд

### Если в таблицах что-то изменилось, то снова сгенерировать миграцию и применить ее.

---

## Работа с авторизацией и jwt-токенами

1. Сначала пользователь регистрируется по ендпоинту /users
2. Далее по ендпоинту /login отправляет данные для получения jwt-токена
3. jwt-токен можно использовать для защищенных роутов (Token Bearer)

---

## Другие рандомные заметки

### Запустить тесты для проекта из корнейвой директории:

```commandline
pytest
```

### Фикстуры

###### Для сохранения данных в фикстуры запустить файл fixtures/load.py

###### Для заполнения бд данными из фикстур запустить файл fixtures/dump.py

### Что доработать/улучшить на досуге)

1. Загрузка/выгрузка фикстур работает не всегда - иногда не видит файл с БД. Либо же найти решение, чтобы избавиться от
   костылей))
2. Написать тесты - исправить структуру проекта + для работы с тестовой БД надо изначально создавать ее по другому
3. Редактировать/удалять данные на роутах могут только те пользователи, которые создавали эти данные

