# MYPKG (TEMPLATE)

MYPKG is a Flask-based API project that manages an imaginary set of elements, in this case called `templates`. It provides CRUD (Create, Read, Update, Delete) operations for template data, utilizing PostgreSQL for persistent storage and Redis for caching and rate limiting.

Key features include:
- RESTful API endpoints for full template management
- Database integration with PostgreSQL for persistent storage
- Caching and rate limiting with Redis
- Prometheus metrics for monitoring
- Logging and tracing capabilities 
- Pre-commit hooks for code quality
- Infrastructure as Code (IaC) pipeline automation with AtlassianBitbucket Pipelines
- Docker (OCI) containerization script
- Job configuration for task scheduling with Hashicorp Nomad

This project is designed with scalability and performance in mind, incorporating best practices for API development and database management.
## DEVELOPMENT PROCESS

### Pre-Commit
Pre-Commit has been installed into this repository as a dependency. In order for the developer to install it as local webhook in the local git repository the developer should execute the following command inside the project's virtual environment:

```
  pre-commit install
```

### Postgres database model (DDL)
For the API to be fully operational is best to create a minimal databae with a single table so evevery endpoint will work as expected.

The database DDL can be as simple as the in-line version that follows:

```
create table templates
(
    tidx        serial
        constraint templates_pk
            primary key,
    templateid  uuid      default gen_random_uuid() not null,
    name        varchar   default ''::character varying,
    description varchar   default ''::character varying,
    content     varchar   default ''::character varying,
    created     timestamp default now(),
    modified    timestamp default now()
);

alter table templates
    owner to root;
```


### Redis database model (DDL)
For the API to be able to accept incoming requests, in the absence of an API Gateway in charge of security controls (AuthN and AuthZ) or routines programmatically written, an API keys routine is `by defualt` in place to ensure a minimal preventative control exists before acessing the API logic. 

Every call to an API endpoint should include an `X-API-KEY` header with its correspondent `UUID4` as value. In order to provide this functionality, a `hash_table` object needs to be created in Redis. A decorator placed over a model function will control the existence of the HTTP header with the API key before processing any request to the named endpoint. 

To create the mentioned hash_table object in Redis, the following command should be executed (assuming that the `redis-cli` command is available in the system or you have the means to pass Redis commands somehow):  

```
HSET sec_apikeys 12345678-90ab-cdef-1234-567890abcdef "user: YourUserOrYourOrgHere"
```


### Environment variables
Create a `.env` file in the project root directory with the configuration variables for databse, among other variables that might also exist there:
```
# -- Use: Flask configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_HOST=localhost
FLASK_PORT=9000

# -- Secret key used by Flask for signatures and sessions
SECRET_KEY="Sup3rC0mpl3xS3cr3tK3y"

# -- Log level in own logging capability but not FLASK_LOG_LEVEL
LOG_LEVEL=DEBUG

# -- Postgres configuration
DB_ENGINE=pg
DB_USER=root
DB_PASS=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mypkg

# -- Redis configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASS=password
REDIS_DB=0
REDIS_MAX_CONN=100

# -- Rate limit settings (unit of measure is: connections per minute)
DEFAULT_RATE_LIMIT=100

# -- Enable or disable Prometheus metrics and sets settings
PROMETHEUS_ENABLED=False
PROMETHEUS_DBLAT_TABLE=templates
PROMETHEUS_DBLAT_COLUMN=templateid

# -- Gunicorn (WSGI) configuration
GUNIPORT=9000

# -- AWS specific settings
AWS_REGION=eu-south-2
AWS_S3_BUCKET=
AWS_S3_BUCKET_PREFIX=

```

A final note should be added in regard to the `LOG_LEVEL` variable: it is not the same as the `FLASK_LOG_LEVEL` variable. It's inteded use is to set the logging level when the function `setup_logging` is called and the `logger.py` module is invoked. In plain few words `the Flask verbose log or debug capability has been disabled and a proper logging mechanism has been put in place instead`. 

The details on the logging levels follows:
``` 
DEBUG (10):
  Detailed information, typically of interest only when diagnosing problems.

INFO (20):
  Confirmation that things are working as expected.

WARNING (30):
  An indication that something unexpected happened, or indicative of some problem in the near future 
  (e.g. 'disk space low'). The software is still working as expected.

ERROR (40):
  Due to a more serious problem, the software has not been able to perform some function.

CRITICAL (50):
  A serious error, indicating that the program itself may be unable to continue running.
```
