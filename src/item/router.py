from fastapi import APIRouter

router = APIRouter(
    tags=["Home"]
)


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get('/items')
async def get_info():
    return 