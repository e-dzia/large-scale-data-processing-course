#!/usr/bin/env bash

pid=$(pidof $1)
if [ ! -z $pid ]
then
	kill $pid
	echo "Process killed!"
else
	echo "No process of this name running"
fi
