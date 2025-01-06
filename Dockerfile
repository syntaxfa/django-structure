FROM python:3.12-slim as builder

LABEL name="alireza feizi" email="alirezafeyze44@gmail.com"
LABEL "website.name"="syntaxfa"
LABEL website="syntaxfa.com"
LABEL desc="This is a python Dockerfile for django projects"

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends && apt-get install -y gettext

WORKDIR /code
COPY . .

RUN pip3 install --upgrade --no-cache-dir pip
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements/production.txt

ENV PYTHONUNBUFFERED=1