#!/bin/bash

export HOST=$(crudini --get app/config.ini main host)
export PORT=$(crudini --get app/config.ini main port)
export PORT_LOCAL=$(crudini --get app/config.ini main port_local)

docker build . -t textarea
docker run -e PORT -e HOST --rm -p $PORT_LOCAL:$PORT textarea
