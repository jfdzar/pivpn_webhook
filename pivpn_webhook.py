import json
import time
import logging
from datetime import datetime, timedelta
import requests

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


if __name__ == "__main__":
    # Read Credentials
    logging.debug("Reading configuration from json file")
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    updateFrequency = credentials['updateFrequency']
    webhook_url = (
        credentials['HA-Url'] +
        credentials['Webhook-Path'] +
        credentials['Webhook-ID']
    )
    clients_list_file = "/data_pivpn_webhook/pivpn_clients.log"

    connected_clients = []

    fast_loop_counter = 60
    fast_loop = 60
    slow_loop_counter = 60 * updateFrequency
    slow_loop = 60 * updateFrequency

    logging.info("Starting Loop")
    while 1:
        time.sleep(1)  # wait
        fast_loop_counter += 1
        slow_loop_counter += 1

        if fast_loop_counter >= fast_loop:
            fast_loop_counter = 0

        if slow_loop_counter >= slow_loop:
            slow_loop_counter = 0

            with open(clients_list_file, 'r') as f:
                output = f.readlines()

            output = output[2:-1]

            new_client_connected = False

            # Split the output into lines and process each line
            for line in output:

                client_info = [x for x in line.split(' ') if x != '']
                name = client_info[0]
                remote_ip = client_info[1]
                virtual_ip = client_info[2]
                bytes_received = client_info[3]
                bytes_sent = client_info[4]
                last_seen_str = (
                    client_info[5] + ' ' +
                    client_info[6] + ' ' +
                    client_info[7] + ' ' +
                    client_info[8] + ' ' +
                    client_info[9].strip()
                )

                logging.debug(name + ' ' + last_seen_str)

                # Parse the last seen time
                last_seen = datetime.strptime(last_seen_str, '%b %d %Y - %H:%M:%S')

                # Check if the client was seen within the last 2 minutes
                if datetime.now() - last_seen <= timedelta(minutes=3):
                    if name not in connected_clients:
                        connected_clients.append(name)
                        logging.debug("New Client connected " + name)
                        new_client_connected = True
                else:
                    if name in connected_clients:
                        connected_clients.remove(name)

            logging.debug(connected_clients)

            if new_client_connected:
                # Notify
                logging.debug("Notify connection")
                new_client_connected = False
                headers = {
                    "Content-Type": "application/json"
                }
                data = {
                    "clients": (';').join(connected_clients)
                }
                response = requests.post(webhook_url, headers=headers, data=json.dumps(data))


    logging.info("Exiting Loop")

    # deepcode ignore replace~exit~sys.exit: 
    # <please specify a reason of ignoring this>
    exit()