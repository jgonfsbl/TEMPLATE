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
PROJECT_NAME="mypkg"
SQITCH_DIR="resources"
ENGINE="pg"
DB_USER="root"
DB_PASS="password"
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="mypkg"
```

## REPOSITORY MANAGEMENT

### Using the Makefile

The Makefile in this project simplifies the management of database migrations and other tasks associated with database setup using Sqitch. Below are the commands available in the Makefile, what they do, and how to use them.

