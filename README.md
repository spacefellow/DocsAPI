## DocsAPI

A simple search engine for the texts of documents. It stores and serves data with Flask, PostgreSQL, Elasticsearch web application.

>Before using app, install elasticsearch and run it in cmd.

### Start the app in Docker

>Download the code
```
$ git clone https://github.com/spacefellow/DocsAPI.git
Create .dbenv and .env files in root folder
$ cd DocsAPI
```

>.flaskenv contains
```
FLASK_APP=./run.py
FLASK_DEBUG=True
DATABASE_URL=some database url
SECRET_KEY=some secret key
ELASTICSEARCH_URL=http://elasticsearch:9200 (for docker setup)
ELASTICSEARCH_URL=http://username:password@localhost:9200 (for Windows setup)
```

>.dbenv contains
```
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=name of database
PGDATA=/var/lib/pgsql/data
```

>Start the APP in Docker
```
$ docker-compose up --build 
```
At this point, the app runs at http://localhost:8000/


### Set Up the app in Windows

>Download the code
```
$ git clone https://github.com/spacefellow/DocsAPI.git
Create .flaskenv file in root folder
$ cd DocsAPI
```

>Install modules VENV
```
$ virtualenv env
$ .\env\Scripts\activate
$ pip install -r requirements.txt
```
>Set Up Flask Environment
```
$ set FLASK_APP=run.py
```

>Start the app
```
Create database 'db name' in PostgreSQL
$ flask db init
$ flask db migrate -m "Some info"
$ flask db upgrade
$ flask run
```
At this point, the app runs at http://127.0.0.1:5000/

To create elements in database move to ...:5000/add

### OpenAPI documentation
```
This application implements swagger for documenting endpoints.
The documentation can be accessed via the url http://.../swagger
```

### Learn More
To learn Flask, check out the [Flask documentation](https://flask.palletsprojects.com/en/2.2.x/).

To learn more about Elasticsearch, check out the [Elasticsearch documentation](https://www.elastic.co/guide/en/elasticsearch/reference/8.4/install-elasticsearch.html)
