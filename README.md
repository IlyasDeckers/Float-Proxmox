Connect to the proxmox API to detect lxc container and collect the required information about them

# Installation
Install the required python modules.
```
pip install python-consul simplejson
```
Copy the git repository to your home folder.
```
cd ~/ && git pull https://github.com/IlyasDeckers/Float-Proxmox && cd Float-Proxmox
```

# Configuration
## config.json

```
mkdir -p /etc/float-proxmox
vi /etc/float-proxmox/config.json

{
    "consul": {
        "address": "127.0.0.1",
        "port": "8500"
    },
    "proxmox": {
        "auth_token": "",
        "host": "hostname",
        "password": "password",
        "port": "8006",
        "username": "username@pve"
    },
    "settings": {
        "log_file": "/var/log/float/float.log",
        "log_level": "INFO"
    }
}
```

## Logging
Create a new directory named float in `/var/log`
```
mkdir -p /var/log/float
touch /var/log/float/float.log
```
