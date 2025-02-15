FROM python:3.12-alpine3.17
LABEL authors="Dell"

ENV PYTHONUNBUFFERED=1

WORKDIR /drf-library-practice

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN adduser -D my_user

RUN chown -R my_user:my_user /drf-library-practice

USER my_user

CMD ["python", "-m", "notification_system.library_bot"]
