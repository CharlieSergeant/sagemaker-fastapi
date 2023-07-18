import logging
from typing import List, Optional
import app.services.evaluation as eval

from fastapi import APIRouter, Depends, HTTPException

from app.core.config import settings

router = APIRouter()

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@router.get('/evaluation')
def get_evaluation_report(
    endpoint_name: str
) -> List:
    return eval.run(endpoint_name)


