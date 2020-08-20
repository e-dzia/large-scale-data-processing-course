#!/usr/bin/env bash

from=$1
to=$2
argc=$#
argv=("$@")

for (( j=2; j<argc; j++ ))
do
	file="${argv[j]}"
	# echo $file
	scp $from/$file $to
done
