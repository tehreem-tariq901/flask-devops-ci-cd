FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache mysql-client gcc musl-dev mariadb-connector-c-dev pkgconfig

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app


ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
