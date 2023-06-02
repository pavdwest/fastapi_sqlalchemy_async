# Overview

A dockerised stack containing the following components:

* FastAPI backend
* Postgres 15 database
* SQLAlchemy ORM (Async)
* Alembic Migrations
* Pydantic Validations

# Getting Started

TODO

1. Clone repo
2. cd
3. pip install for local dev
4. docker compose up --build
5. Set up pgAdmin4
6. Run once docker compose up --build attach backend
7. Check localhost:8000/docs
8. Init alembic: `docker compose exec <fastapi_pg_sqlalchemy-backend-1> alembic init -t async src/migrations`
