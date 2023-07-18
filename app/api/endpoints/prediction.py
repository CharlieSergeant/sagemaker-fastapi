import logging
from typing import List, Optional
from app.services.pipeline import run
from app.schemas.input_object import InputObject
from fastapi import APIRouter, Depends, HTTPException
from app.core.config import settings

router = APIRouter()

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


@router.get("/healthcheck")
def healthcheck():
    return "AWAKE"


@router.post('/prediction')
def get_prediction(
        input_objects: List[InputObject],
        endpoint_name: str,
        model_name: str = None,
        model_type: str = 'mme'
) -> List:
    return run(
        input_objects=input_objects,
        endpoint_name=endpoint_name,
        model_name=model_name,
        model_type=model_type
    )
