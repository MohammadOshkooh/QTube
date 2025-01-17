FROM docker.arvancloud.ir/python:3.10.12

# set work dir
WORKDIR /code/back

# # set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1


# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1


RUN apt-get update

# install dependencies
COPY requirements.txt /code/back/
RUN pip install --upgrade pip && pip install -r requirements.txt


# copy project
COPY . /code/back/