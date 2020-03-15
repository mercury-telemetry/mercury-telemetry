# CommunicationsPi

### This directory contains all the scripts related to communications via LAN, Radio and internet.

Note: `env` file contains environment variables required to run different services. Please run the following command to
export variables before running any service.

```
  cd hardware
  if [ -f env ]; then export $(cat env | sed 's/#.*//g' | xargs); fi
```
