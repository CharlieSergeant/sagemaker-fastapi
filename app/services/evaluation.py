import boto3

from app.core.config import settings
from app.core.utils import get_endpoint, read_s3_csv


def run(
    endpoint_name: str,
):
    try:

        endpoint = get_endpoint(endpoint_name_filter=endpoint_name)
        if endpoint is None:
            raise Exception(f'Endpoint for {endpoint_name} does not exist')

        evaluation_data_bucket = settings.OUTPUT_BUCKET
        # **********************************************
        # Add Evaluation Report prefix
        # **********************************************
        evaluation_data_prefix = ''

        s3_resource = boto3.resource('s3')
        bucket_obj = s3_resource.Bucket(evaluation_data_bucket)
        evaluations = [i.key.replace(evaluation_data_prefix, '').replace('.csv','') for i in bucket_obj.objects.filter(Prefix=evaluation_data_prefix) if '.csv' in i.key]
        sorted(evaluations)
        latest = evaluations[-1]
        df = read_s3_csv(evaluation_data_bucket,evaluation_data_prefix+latest+'.csv')
        return df.to_dict(orient='records')
    except Exception as e:
        raise e
