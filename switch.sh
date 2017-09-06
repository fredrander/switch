#!/bin/bash

if [ "$1" = "--start" ]; then

    cd /home/switch/

    python -B main.py &
    echo $! > .switchpid

    echo Started
    cat .switchpid

elif [ "$1" = "--stop" ]; then

    cd /home/switch/
    
    echo Stop
    cat .switchpid

    for p in $(cat .switchpid); do 
        kill -9 $p 
    done
        rm .switchpid

else

    echo ERROR

fi


