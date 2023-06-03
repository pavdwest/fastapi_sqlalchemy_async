# Overview

A dockerised multi-tenant (by schema) stack containing the following components:

* FastAPI backend
* Postgres 15 database
* SQLAlchemy ORM (Async)
* Alembic Migrations
* Pydantic Validations

# Getting Started

TODO

1. Clone repo:

    ```git clone git@github.com:pavdwest/fastapi_pg_sqlalchemy.git```

2. Enter directory:

    ```cd fastapi_pg_sqlalchemy```

3. Create virtual environment:

    ```python -m venv services/backend/app/.ignore/venv```

4. Install dependencies for local development/intellisense:

    ```pip install -r services/backend/app/requirements/base.txt```

5. Run stack (we attach only to the backend as we don't want to listen to PGAdmin4 spam):

    ```docker compose up --build --attach backend```

6. Everything's running:

    ```http://127.0.0.1:8000/docs```

7. Run migrations with Alembic:

     ```docker compose exec fastapi_pg_sqlalchemy-backend-1 alembic upgrade head```

# Notes

## Set up Alembic from scratch:

```docker compose exec fastapi_pg_sqlalchemy-backend-1 alembic init -t async src/migrations```
