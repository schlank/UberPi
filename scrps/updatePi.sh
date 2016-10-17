#!/bin/bash

cd ~/UberPi
git pull
pkill -f piControls.py
python piControls.py
