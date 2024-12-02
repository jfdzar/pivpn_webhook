# Introduction

Monitor my PiVPN instance and send a notification via Homeassistant using a webhook

Based on previous repository pivpn_mqtt and on this post of the homeassistant forum
https://community.home-assistant.io/t/send-pivpn-client-info-to-ha-with-mqtt/206765

I got the code and change it a bit to fulfill my purpose

# Instructions for use
Clone the repository

Rename credentials_example.json to credentials.json and modify it with your credentials

Build the docker container with the command below 
```bash
docker build -t pivpn_webhook .
```

Modify the docker-compose.yml if needed with correct location of the volumes

Before starting the docker container a cronjob must be started.
This cronjob run the needed pivpn command and put the output in a log file.
The python script in the docker container then read this files.
This way we can have the script running in a docker container without affecting the host python environment

```bash
*/3 * * * * /usr/local/bin/pivpn -c > ~/pivpn_webhook/data/pivpn_clients.log 2>&1
```
additionally create a folder in the repository called data to save the logs

Start the container with docker compose

```bash
docker compose up -d
```



# Extra Docker commands
A list of commands to debug intersting to use

```bash
docker run --restart=unless-stopped -v ~/pivpn_webhook/data:/data_pivpn_webhook --name pivpn_webhook pivpn_webhook

docker rm pivpn_webhook

docker stop pivpn_webhook

docker exec -it pivpn_webhook /bin/sh
```
