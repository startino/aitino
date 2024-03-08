#!/usr/bin/sh

docker run --name "redis" --rm -it -p 6379:6379 redis:5-alpine