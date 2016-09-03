#!/bin/bash
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
   printf "My IP Address is %s\n" $_IP
fi

exit 0
