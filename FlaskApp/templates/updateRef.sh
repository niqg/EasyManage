#!/bin/bash

if [ "$1" != "" ]; then
    sudo touch temp
    sudo chmod 777 temp
    cat $1 | grep '\\(?:.(?!\\))+\.js' > temp
	
else
    echo "Please specify an html file to perform updating of"
fi
