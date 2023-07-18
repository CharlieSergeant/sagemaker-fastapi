from fastapi import APIRouter

from app.api.endpoints import prediction
from app.api.endpoints import evaluation

api_router = APIRouter()
api_router.include_router(prediction.router)
api_router.include_router(evaluation.router)
