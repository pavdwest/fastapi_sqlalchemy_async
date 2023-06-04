from typing import Dict

from fastapi import APIRouter, status, Response


router = APIRouter(
    tags=['Home']
)


@router.get(
    '/home',
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    summary='Returns 200 if service is up and running',
    description='Endpoint description. Will use the docstring if not provided.',
)
async def home(response: Response) -> Dict:
    """
    Home

    Args:
        response (Response): Ignore, it's for internal use.

    Returns:
        Dict: {
            'message': 'Hello boils and ghouls'
        }
    """
    return {
        'message': 'Hello boils and ghouls'
    }


@router.get(
    '/sandbox',
    status_code=status.HTTP_200_OK,
    summary='Returns 200 if service is up and running',
    description='Endpoint description. Will use the docstring if not provided.',
)
async def sandbox():

    from src.database.service import db
    db.clone_db_schema(source_schema_name='tenant', target_schema_name='xantghar')


    return {
        'msg': 'asdsad'
    }
