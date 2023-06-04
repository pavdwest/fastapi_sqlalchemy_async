from fastapi import APIRouter, status


router = APIRouter(
    tags=['Sandbox']
)


@router.get(
    '/sandbox',
    status_code=status.HTTP_200_OK,
    summary='Sandbox endpoint',
    description='Endpoint description. Will use the docstring if not provided.',
)
async def sandbox():

    return {
        'msg': 'sandbox'
    }
