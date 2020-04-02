# CommunicationsPi

### This directory contains all the scripts related to communications via LAN, Radio and internet.

Note: `env` file contains environment variables required to run different services. Please run the following command to
export variables before running any service.

```
  cd hardware
  if [ -f env ]; then export $(cat env | sed 's/#.*//g' | xargs); fi
```

##### Scripts
- `lan_client.py`: Sends post data via LAN to Local LAN server
- `lan_server.py`: Listens to LAN clients
- `serial_write.py`: Sends data via radio serial
- `serial_read.py`: Listens to radio serial
