import json
import logging
import re
from io import BytesIO

import boto3
import pandas as pd
import requests
from app.core.config import settings

def read_s3_csv(bucket, s3_key):
    '''
    Download from S3
    '''
    try:
        s3_client = boto3.client('s3')
        obj = s3_client.get_object(Bucket=bucket, Key=s3_key)
        df = pd.read_csv(BytesIO(obj['Body'].read()))
    except FileNotFoundError as e:
        logging.error(f'file not found at {bucket}/{s3_key} {e}')
        return pd.DataFrame()
    except Exception as e:
        logging.error(f'error for {bucket}/{s3_key} {e}')
        return pd.DataFrame()
    return df

# CRUD Sagemaker Endpoints
def get_endpoints(endpoint_name_filter,sagemaker_client = None):
    if sagemaker_client is None:
        sagemaker_client = boto3.client("sagemaker", region_name='us-west-2')
    # Retrieve all endpoints for filtered name
    response = sagemaker_client.list_endpoints(SortBy='Name', NameContains=endpoint_name_filter, MaxResults=100)
    sagemaker_endpoints_for_service = response["Endpoints"]
    # AWS request pagination
    while "NextToken" in response:
        response = sagemaker_client.list_endpoints(NextToken=response["NextToken"], SortBy='Name',
                                                   NameContains=endpoint_name_filter, MaxResults=100)
        sagemaker_endpoints_for_service.extend(response["Endpoints"])
    endpoints = []
    for i in sagemaker_endpoints_for_service:
        endpoints.append(i['EndpointName'])
    if len(endpoints) == 0:
        print(f"No Endpoints found for filter: {endpoint_name_filter}")
    return endpoints


def get_endpoint(endpoint_name_filter, sagemaker_client = None):
    if sagemaker_client is None:
        sagemaker_client = boto3.client("sagemaker", region_name='us-west-2')
    endpoints = get_endpoints(endpoint_name_filter,sagemaker_client=sagemaker_client)
    if len(endpoints) == 0:
        return None
    else:
        return endpoints[0]

def get_models_on_endpoint(model_data_prefix):
    s3_resource = boto3.resource('s3')
    bucket_obj = s3_resource.Bucket(settings.ARTIFACTS_BUCKET)
    prefix = model_data_prefix.replace(f's3://{settings.ARTIFACTS_BUCKET}/','')
    try:
        models_on_endpoint = [i.key.replace(prefix, '') for i in bucket_obj.objects.filter(Prefix=prefix)]
        return models_on_endpoint
    except Exception as e:
        logging.error(f" --- Failed to get models on endpoint ---- {e}")
        models_on_endpoint = []
        return models_on_endpoint

def get_model_on_endpoint(model_data_prefix,model_substring='',latest=None):
    '''
    The model string is returned if the substring of the model we are looking for is on the endpoint
    :param model_substring:
    :return:
    '''
    models_on_endpoint = get_models_on_endpoint(model_data_prefix)
    if latest is not None:
        sorted(models_on_endpoint)
        return models_on_endpoint[0]
    res = None
    for model in models_on_endpoint:
        if model_substring in model:
            res = model
            break
    return res

def clean_string(s):
    if isinstance(s, str):
        return re.sub("[\W_]+",'',s)
    else:
        return s