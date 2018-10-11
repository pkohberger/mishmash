FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD ./src/ /code/
RUN apt-get update && apt-get install nano -y && python -m pip install --no-binary :all: -r /code/requirements.txt