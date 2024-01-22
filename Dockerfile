FROM python:3.10

EXPOSE 8008

COPY src /app
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

RUN adduser --disabled-password app-user

USER app-user
