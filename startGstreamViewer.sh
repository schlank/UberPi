#!/bin/bash

#gst-launch-1.0 -v tcpclientsrc host=10.215.50.40 port=5000 ! gdpdepay ! rtph264depay !  ! autovideosink sync=false
#gst-launch-1.0 tcpclientsrc host=10.215.50.40 port=5000 ! decodebin ! videoconvert ! autovideosink sync=false
gst-launch-1.0 -v tcpclientsrc host=10.215.50.46 port=5000 ! gdpdepay !  rtph264depay ! avdec_h264 ! videoconvert ! autovideosink sync=false
