# Don't move this file into another directory! Relative app folders are determined from it!
import os

from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# Project
PROJECT_NAME = os.environ.get('PROJECT_NAME')

# Project folders
APP_SRC_FOLDER_ABS = os.path.dirname(os.path.realpath(__file__))

# Redis
REDIS_HOST     = os.environ.get('REDIS')
REDIS_PORT     = os.environ.get('REDIS_PORT')
REDIS_USERNAME = os.environ.get('REDIS_USERNAME')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

# Database
def create_database_url(
    database_adapter: str,
    database_host: str,
    database_port: int,
    database_username: str,
    database_password: str,
    database_name: str,
) -> str:
    """
    Generates a connection string.
    Note that you can't use special characters in any of these params - they are not escaped properly!

    Args:
        database_adapter (str): e.g. `psycopg2` or `asyncpg`
        database_host (str): e.g. `localhost` or `127.0.0.1`
        database_port (int): e.g. `5432`
        database_username (str): e.g. `postgres_user` or `admin`
        database_password (str): e.g. `superSecur3pAs5w0Rd`
        database_name (str): e.g. `postgres` or `my_app_db`

    Returns:
        str: A string of the form `postgresql+asyncpg://postgres_user:superSecur3pAs5w0Rd@127.0.0.1:5432/my_app_db`
    """
    return f"postgresql+{database_adapter}://{database_username}:{database_password}@{database_host}:{database_port}/{database_name}"

SHARED_SCHEMA_NAME: str = 'shared'
TENANT_SCHEMA_NAME: str = 'tenant'
DATABASE_POOL_SIZE: int = 12
DATABASE_HOST: str      = os.environ.get('DATABASE_HOST')
DATABASE_PORT: int      = os.environ.get('DATABASE_PORT')
DATABASE_USERNAME: str  = os.environ.get('DATABASE_USERNAME')
DATABASE_PASSWORD: str  = os.environ.get('DATABASE_PASSWORD')
DATABASE_NAME: str      = os.environ.get('DATABASE_NAME')
DATABASE_URL_SYNC: str  = create_database_url(
    database_adapter  = 'psycopg2',
    database_host     = DATABASE_HOST,
    database_port     = DATABASE_PORT,
    database_username = DATABASE_USERNAME,
    database_password = DATABASE_PASSWORD,
    database_name     = DATABASE_NAME,
)
DATABASE_URL_ASYNC: str  = create_database_url(
    database_adapter  = 'asyncpg',
    database_host     = DATABASE_HOST,
    database_port     = DATABASE_PORT,
    database_username = DATABASE_USERNAME,
    database_password = DATABASE_PASSWORD,
    database_name     = DATABASE_NAME,
)

# Auth
JWT_SECRET_KEY         = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']
ACCESS_TOKEN_EXPIRE_MINUTES  = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
