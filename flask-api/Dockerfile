FROM python:3.10-slim

# allows statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED TRUE

# copy local code to container image
ENV APP_HOME /flask-api
WORKDIR $APP_HOME 
COPY . ./

RUN apt-get update && apt-get install -y ffmpeg
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app


