FROM python:3.9


WORKDIR /src/server

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./requirements.txt /src/server/

RUN pip3 install --upgrade pip && \
    pip3 install --upgrade -r /src/server/requirements.txt
