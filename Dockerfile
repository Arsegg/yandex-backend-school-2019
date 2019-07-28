FROM python:3.7.4-alpine

ENV FLASK_APP=app.py
WORKDIR /app

ADD requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

ADD . .
ENTRYPOINT ["flask", "run"]
