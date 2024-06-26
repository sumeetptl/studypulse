# pull official base image
FROM python:3.12.4-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt
# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# copy project
COPY . .

