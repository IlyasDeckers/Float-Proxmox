Register proxmox LXC containers as a service in Consul. 

# Configuration
## config.json
Edit the configuration file found in this repo in `Float-Proxmox/etc/float-proxmox/config.json`

NOTE: Leave the auth_token empty this will be generated automatically.
```
cd Float-Proxmox
vi etc/float-proxmox/config.json
```
example:
```
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

# Installation
Copy the git repository to your home folder.
```
cd ~/ && git pull https://github.com/IlyasDeckers/Float-Proxmox && cd Float-Proxmox
```

## Standalone
```
sudo mkdir /etc/float-proxmox 
sudo cp etc/float-proxmox/config.json /etc/float-proxmox/

ln -s usr/local/bin/float-proxmox /usr/local/bin/float-proxmox
```
Create a System V init script to start and stop Float-Proxmox and reload the configuration.
```
vi /etc/init.d/float-proxmox
```
Copy the script below:
```

#!/bin/sh

### BEGIN INIT INFO
# Provides:          myservice
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Put a short description of the service here
# Description:       Put a long description of the service here
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
DIR=/usr/local/bin/
DAEMON=$DIR/float-proxmox
DAEMON_NAME=float-proxmox

# Add any command line options for your daemon here
DAEMON_OPTS=""

# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=root

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
```

## Docker container
