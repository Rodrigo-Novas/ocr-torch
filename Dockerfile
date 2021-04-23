FROM python:3.7-alpine

WORKDIR /home

ENV FLASK_RUN_HOST 0.0.0.0

ENV FLASK_APP __main__.py

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "flask", "run" ]