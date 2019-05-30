#!/bin/bash

#python3 audio_receive.py 2> /dev/null &
#python3 qr_receive.py 2> /dev/null &

python3 audio_receive.py &
python3 qr_receive.py &

