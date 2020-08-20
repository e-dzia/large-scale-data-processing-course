#!/usr/bin/env bash

num_lines=$1
if [ -z "$num_lines" ]
then
	num_lines=10
fi
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 100 | head -n $num_lines
echo ""
