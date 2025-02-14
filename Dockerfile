FROM python:3.12-alpine3.17
LABEL authors="Dell"

ENV PYTHONUNBUFFERED=1

WORKDIR /drf-library-practice
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN mkdir -p /files/media

RUN mkdir -p /app
RUN touch /app/celerybeat-schedule

RUN adduser -D my_user
RUN chown -R my_user /files/media
RUN chown my_user /app/celerybeat-schedule
RUN chown -R my_user /drf-library-practice
RUN chmod 775 /app/celerybeat-schedule
RUN chmod -R 775 /drf-library-practice

USER my_user