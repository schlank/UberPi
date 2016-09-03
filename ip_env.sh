#!/bin/bash
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
   printf "My IP Address is %s\n" $_IP
   export UBER_HOST=$_IP
   echo $UBER_HOST
fi
exit 0
