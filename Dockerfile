FROM python:3.8.8-slim-buster

RUN apt-get update \
    && apt-get install -y make \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /inet-trouble-ml-api

WORKDIR /inet-trouble-ml-api

ENV FLASK_ENV=development
ENV FLASK_APP=wsgi.py

COPY . /inet-trouble-ml-api

RUN pip install pip==21.0.1
RUN pip install setuptools==54.1.2
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["flask", "run"]
