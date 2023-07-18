from io import StringIO

import boto3
import json

import numpy as np
import pandas as pd

from app.core.config import settings

def get_predictions(requests, endpoint_name, model_name,model_type='mme'):
    '''
    Pass preprocessed requests to the specific endpoint (mme or single)
    '''
    sagemaker_runtime = boto3.client("sagemaker-runtime", region_name=settings.REGION)
    responses = []
    for request in requests:
        if model_type == 'mme':
            response = sagemaker_runtime.invoke_endpoint(
                ContentType='application/json',
                EndpointName=endpoint_name,
                TargetModel=model_name,
                Body=json.dumps(request)
            )
            res = json.loads(response['Body'].read().decode('utf-8'))[0]
        else:
            # XGBoost by default does not allow application/json
            response = sagemaker_runtime.invoke_endpoint(
                ContentType='csv',
                EndpointName=endpoint_name,
                Body=pd.DataFrame(data=[request]).to_csv(index=False,header=False)
            )
            res = float(response['Body'].read().decode('utf-8'))
        responses.append(res)
    return responses
