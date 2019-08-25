FROM python:3.7.4-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev py3-numpy

ENV FLASK_APP=app.py
WORKDIR /app

ADD requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

ADD . .
ENTRYPOINT ["flask", "run"]
