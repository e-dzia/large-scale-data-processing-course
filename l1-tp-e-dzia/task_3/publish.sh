#!/usr/bin/env bash

path=$1
name=$2
if [ -z "$name" ]
then
	name=test
fi

if [ ! -z "$path" ]
then
	timestamp="$(date +"%s")"

	docker build -t $name $path
	docker tag $name edzia/$name:$timestamp
	docker push edzia/test
fi
