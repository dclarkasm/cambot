#!/bin/sh
# Installs dependencies for autogram

sudo apt-get install ssmtp python3-yaml -y
sudo apt-get install python-picamera python3-picamera -y

python3 -m pip install cryptography
