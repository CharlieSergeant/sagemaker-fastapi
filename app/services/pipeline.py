from typing import List

import boto3
from app.services.preprocess import do_preprocess
from app.services.inference import get_predictions
from app.services.postprocess import do_postprocessing
from app.core.utils import get_endpoint
from app.schemas.input_object import InputObject


def run(
    input_objects: List[InputObject],
    endpoint_name: str,
    model_name=None,
    model_type='mme'
):
    '''
     Process the input inferences and get predictions from the sagemaker endpoint
    :param inferences:
    :param endpoint_name:
    :param model_name:
    :param model_type:
    :return: List[Predictions]
    '''

    endpoint = get_endpoint(endpoint_name_filter=endpoint_name)
    if endpoint is None:
        raise Exception(f'Endpoint for {endpoint_name} does not exist')

    # If we dont have a model_name default is endpoint name
    if model_name is None:
        model_name = endpoint_name

    preprocessed_df = do_preprocess(
        input_objects
    )
    model_responses = get_predictions(
        preprocessed_df.values.tolist(),
        endpoint_name,
        model_name,
        model_type=model_type
    )
    predictions = do_postprocessing(
        model_responses
    )
    return predictions

