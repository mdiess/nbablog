#!/usr/bin/env bash

source environment.sh

# run
if [ "$1" == pg:backups ]; then
	if [ -z ${3+x} ]; then
		echo "Usage: $1 <user> <db>"
	else
		heroku pg:backups:capture --app marchsl
		curl -o latest.dump `heroku pg:backups:public-url --app marchsl`
		echo "User: $2   DB: $3"
		pg_restore --verbose --clean --no-acl --no-owner -j 2 -h localhost -U $2 -d $3 latest.dump
	fi
elif [ "$1" == pg_restore ]; then
	if [ -z ${3+x} ]; then
		echo "Usage: $1 <user> <db>"
	else
		echo "User: $2   DB: $3"
		pg_restore --verbose --clean --no-acl --no-owner -j 2 -h localhost -U $2 -d $3 latest.dump
	fi
elif [ "$1" == runserver -a "$2" == -i ]; then
	ip=`hostname -I | awk '{print $1}'`
	port="8000"
	arg="$ip:$port"
	./manage.py $1 $arg $3
else
	./manage.py $@
fi