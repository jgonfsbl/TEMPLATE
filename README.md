# TEMPLATE

Project template description comes here. 

## DEVELOPMENT PROCESS

### Pre-Commit
Pre-Commit has been installed into this repository as a dependency. In order for the developer to install it as local webhook in the local git repository the developer should execute the following command inside the project's virtual environment:

```
  pre-commit install
```

### Environment variables and database migrations
Create a `.env` file in the project root directory with the configuration variables for databse, among other variables that might also exist there:

```
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_HOST=127.0.0.1
export FLASK_PORT=9000
export FLASK_LOG_LEVEL=DEBUG
export FLASK_SECRET_KEY="Sup3rC0mpl3xS3cr3tK3y"

export X_API_KEY=c4dd4532-6275-4b51-bb18-d84e7ac3262e

export GUNIPORT=5000

export PROJECT_NAME=mypkg
export SQITCH_DIR=resources
export DB_ENGINE=pg
export DB_USER=root
export DB_PASS=password
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=mypkg
```

## REPOSITORY MANAGEMENT

### Using the Makefile

The Makefile in this project simplifies the management of database migrations and other tasks associated with database setup using Sqitch. Below are the commands available in the Makefile, what they do, and how to use them.

