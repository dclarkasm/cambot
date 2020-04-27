# cambot
A simple Python script to take a picture every day at sunrise and send it in an email.

Run setup.sh:
> $ setup.sh

Configure ssmtp: http://tombuntu.com/index.php/2008/10/21/sending-email-from-your-system-with-ssmtp/

## Files:
`main.py`: This is the code that controls the sleep cycle system. It is intended to run on the Adafruit Gemma M0 (Not the Raspberry Pi).
`cambot.py`: This is the script that takes the pictures and emails them. This runs on the Raspberry Pi.
`rc.local`: This file is needed to run `cambot.py` automatically on boot. It should be copied to /etc/rc.local.

Run autogram
