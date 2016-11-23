#!/bin/bash
SERVICE="node"
RESULT=`ps -a | sed -n /${SERVICE}/p`

if [ "${RESULT:-null}" = null ]; then
   echo "Starting Node"
   cd ~/Desktop/alexa-avs-sample-app/samples/companionService
   lxterminal\
   --title="Node Alexa Server" \
   -e "npm start"
else
   echo "node already running"
fi

echo "Java client trying a start"

SERVICE="java"
RESULT=`ps -a | sed -n /${SERVICE}/p`
if [ "${RESULT:-null}" = null ]; then
   sleep 15s;
   echo "java Client Starting"
   cd ~/Desktop/alexa-avs-sample-app/samples/javaclient
   lxterminal\
   --title="Alexa Java Client" \
   -e "mvn exec:exec"
   sleep 35s;
else
   echo "Java Client already running"
fi

echo "Java Client already running"

cd ~/Desktop/alexa-avs-sample-app/samples/wakeWordAgent/src

lxterminal\
   -title="MyScriptWindow" \
   -e "./wakeWordAgent -e sensory"
