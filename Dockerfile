# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

WORKDIR /pivpn_webhook

RUN apt-get update && apt-get install libsm6 libxext6 -y

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime

COPY . .

CMD [ "python3", "pivpn_webhook.py"]