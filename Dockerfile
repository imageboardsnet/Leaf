# syntax=docker/dockerfile:1
FROM python:3.12-alpine
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
COPY static /code
COPY templates /code

RUN mkdir -p /code/articles

CMD ["gunicorn", "-b", "0.0.0.0:6000", "app:create_app()"]
