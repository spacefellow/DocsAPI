## RUSSPASS HACKATHON

This solution used technologies such as: FastApi, PostgreSQL, Sklearn, Pandas. The latter were used to implement a collaborative recommendation system for users.


### Start the app in Docker

>Download the code
```
$ git clone https://github.com/Svogg/xakaton
Create .dbenv and .env_dev files in root folder
$ cd xakaton
```

>.env_dev contains
```
SECRET_KEY=some secret key
```

>.dbenv contains
```
POSTGRES_DRIVER=postgresql
POSTGRES_CONNECTOR=asyncpg
POSTGRES_USER=user
POSTGRES_PASS=pass
POSTGRES_HOST=DATABASE
POSTGRES_PORT=5432
DB_NAME=db_name
```

>Make docker images
```
$ docker-compose build
$ docker-compose up -d
```

>Create database in db_container
```
$ docker-compose exec -it database psql —host database -U
$ CREATE DATABASE db_name;
```

>Create alembic migrations in the backend_container and load data into the database
```
$ docker-compose exec -it backend bash
$ alembic init migrations
$ alembic revision --autogenerate -m "initial"
$ alembic upgrade HEAD
$ python dbinit.py
```

At this point, the backend runs at http://localhost:8000/
Frontend runs at http://localhost:8000/
