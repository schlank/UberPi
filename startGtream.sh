#!/bin/bash

#Later installs
#sudo apt-get install espeak

raspivid -fps 25 -h 600 -w 800 -vf -hf -n -t 0 -b 2000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=10.215.50.46 port=5000
#cd ~/Uberpi/
#python robotwkeyboard
