#!/bin/sh

docker network create mynetwork

docker build -t twitter_server:latest -f server/Dockerfile .
docker build -t twitter_client:latest -f client/Dockerfile .

# sp