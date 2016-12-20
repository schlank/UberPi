#!/bin/bash

SERVICE="node"
RESULT=`ps -a | sed -n /${SERVICE}/p`
NODE_STARTING=false
if [ "${RESULT:-null}" = null ]; then
   echo "Starting Node"
   cd ~/alexa-avs-sample-app/samples/companionService
   lxterminal\
   --geometry=50x50 \
   --title="Node Alexa Server" \
   -e "npm start"
   NODE_STARTING=true
else
   echo "node already running"
fi

echo "Java client trying a start"

SERVICE="java"
RESULT=`ps -a | sed -n /${SERVICE}/p`
if [ "${RESULT:-null}" = null ]; then
   if [ "$NODE_STARTING" = true ]; then
   	sleep 15s;
   fi
   echo "java Client Starting"
   cd ~/alexa-avs-sample-app/samples/javaclient
   lxterminal\
   --title="Alexa Java Client" \
   --geometry=80x50 \
   -e "mvn exec:exec"
   sleep 35s;
else
   echo "Java Client already running"
fi

echo "Starting Wake Word Agent"

cd ~/alexa-avs-sample-app/samples/wakeWordAgent/src

lxterminal\
   --title="Wake Word Agent" \
   --geometry=80x50 \
   -e "./wakeWordAgent -e sensory"
