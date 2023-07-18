import logging
import time
from datetime import timedelta, datetime

import boto3
from pickle import dumps, loads
from io import BytesIO
import pandas as pd
import numpy as np

import h3.api.numpy_int as h3
from app.core.config import settings
from app.core.utils import read_s3_csv, clean_string
from fastapi.encoders import jsonable_encoder

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

"""
Preprocessing functions

Helper Transformation functions on raw company data to prepare data for training
"""

def apply_h3_regions(df):
    '''
    Perform large (US Region), mid (US State), small (US City), and id (specific location)
    H3 Index magnifications are hexagonal mapped regions
    '''
    df['h3largeregion'] = h3.geo_to_h3(df['latitude'], df['longitude'], 0)
    df['h3midregion'] = h3.geo_to_h3(df['latitude'], df['longitude'], 2)
    df['h3smallregion'] = h3.geo_to_h3(df['latitude'], df['longitude'], 5)
    df['h3idregion'] = h3.geo_to_h3(df['latitude'], df['longitude'], 14)
    return df


def do_preprocess(inferences):
    '''
    Turn raw payload data into model ready data
    - Timeseries feature engineering
    - Location based features using Uber's H3
    - Data imputation
    '''
    try:
        inference_df = pd.DataFrame(jsonable_encoder(inferences))
        inference_df.columns = [clean_string(col.lower()) for col in inference_df.columns.values]
        # *********************************************
        # Add business related preprocessing logic here
        # *********************************************
        return inference_df
    except Exception as e:
        logging.error('Failure in Preprocessing ',exc_info=e)
        return



