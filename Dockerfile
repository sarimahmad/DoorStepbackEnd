FROM python:3.9-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk del .tmp
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
