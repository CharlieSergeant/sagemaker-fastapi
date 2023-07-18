# SageMaker FastAPI

## Overview

The SageMaker FastAPI project provides a seamless way to preprocess data, invoke a SageMaker endpoint hosted on AWS, and perform postprocessing on the prediction results. This project is designed to be a user-friendly and efficient solution for handling machine learning tasks with Amazon SageMaker using FastAPI, a modern web framework for building APIs in Python. 

**Please Note:** This project generates a scaffold to follow common machine learning workflows and will need to be extended to a certain business use case

## Requirements

- AWS-CLI: Before getting started, make sure you have the AWS Command Line Interface (CLI) installed and properly configured with your AWS credentials.
- Python Virtual Environment: We recommend creating a virtual environment to manage the project dependencies. To set up the virtual environment, run `pip install -r requirements.txt` inside the virtual environment.
- Docker: If you plan to deploy your application in a containerized environment, ensure that Docker is installed on your system.

## Usage

1. Clone the repository and navigate to the project directory.

2. Configure [AWS-CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) with your AWS credentials to ensure seamless interaction with AWS and SageMaker resources.

3. Install project dependencies using the following command inside your Python virtual environment:

   ```bash
   pip install -r requirements.txt
   ```
4. Extend to your use case:
   1. ```app/schemas/input_object.py```: Build Object that will be passed into the API via post request
   2. ```app/services/preprocess.py```: Add custom data transformation logic to convert raw object to model ready data
   3. ```app/services/postprocess.py```: Add custom data transformation logic to convert model response to user ready data
   4. ```app/services/evaluation.py```: Add prefix path to model evaluation reports (expects csv format)
5. To run the FastAPI API server (locally), execute the following command:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0
   ```

   The API documentation will be available at http://localhost:8000/docs. Use this documentation to understand the available endpoints and their input/output formats.
6. Build and Run Docker
    ```bash
    docker build -t sagemaker-fastapi .
    docker run -d -p 8000:8000 sagemaker-fastapi uvicorn app.main:app --host 0.0.0.0 --port 8000
    ```
## Pipeline

The SageMaker FastAPI project provides a ```app/services/pipeline.py``` to handle three main steps of the machine learning process: preprocessing, inference, and postprocessing. Which is called from the prediction api.

### 1. Preprocessing

To transform raw order data into model-ready data, use `app/services/preprocess.py`. This script processes the input data and prepares it for inference by the SageMaker model.

### 2. Inference

The `app/services/inference.py` script is used to invoke a hosted SageMaker Multi Model Endpoint and obtain predictions from the model. The script handles communication with the SageMaker endpoint and receives the inference results.

### 3. Postprocessing

After obtaining the model predictions, you can use `app/services/postprocess.py` to transform the raw prediction data into user-friendly responses. This step ensures that the API delivers results in a format suitable for consumption by end-users.

## Evaluation

The project also provides an `app/services/evaluation.py` script to run an evaluation job on the model. This script enables you to assess the model's performance by running evaluation tests against the SageMaker endpoint. The evaluation endpoint offers valuable performance metrics for the model.

## Extensions

### Database Connection 
1. Add evaluation metrics to a postgres db
2. Add input objects to postgres db to call directly from database and avoid passing data attributes in a post request
3. Add predictions table to store a cached version of predictions already called 

### Other ML Solutions

Just replace the logic from the `app/services/inference.py` to whatever ML hosting platform you are using. All logic is currently configured using boto3 (AWS Python API) to invoke an AWS hosted SageMaker model

1. [Google Cloud AI Platform](https://cloud.google.com/ai-platform/docs/technical-overview)

2. [Microsoft Azure Machine Learning](https://azure.microsoft.com/en-us/services/machine-learning/)

3. [IBM Watson Studio](https://www.ibm.com/cloud/watson-studio)

4. [Databricks](https://databricks.com/solutions/machine-learning)

5. [H2O.ai](https://www.h2o.ai/)

6. [MLflow](https://mlflow.org/)

7. [Apple Core ML](https://developer.apple.com/documentation/coreml)

8. [Kubeflow](https://www.kubeflow.org/)

### Local Blob Storage
1. [Minio](https://min.io/): Open Source, Amazon S3 compatible, Kubernetes Native and is designed for cloud native workloads like AI.

## References:
- [FastAPI](https://fastapi.tiangolo.com/)
- [SageMaker](https://aws.amazon.com/sagemaker/)
- [SageMaker Examples](https://github.com/aws/amazon-sagemaker-examples)
- [Boto3 SageMaker](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker.html)

