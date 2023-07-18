FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Warning the uvicorn docker image expects the app to be in /app/app/main.py
COPY requirements.txt /app
RUN pip3 install -r /app/requirements.txt
COPY ./app /app/app

