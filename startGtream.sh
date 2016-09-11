#!/bin/bash

#Later installs
#sudo apt-get install espeak

_IP=$(hostname -I) || true
if [ "$_IP" ]; then
   printf "My IP Address is %s\n" $_IP
   espeak "IP Address is ${_IP}"
   UBER_HOST=$_IP
   UBER_PORT=9036
   echo $UBER_HOST
   raspivid -fps 25 -h 600 -w 800 -vf -hf -n -t 0 -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=$UBER_HOST port=$UBER_PORT
fi
