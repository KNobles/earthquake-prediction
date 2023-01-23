#!/bin/sh

docker network create mynetwork;
docker-compose build && docker-compose up;