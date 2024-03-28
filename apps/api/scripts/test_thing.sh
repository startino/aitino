#!/usr/bin/env bash

ENDPOINT="https://api.aiti.no/openapi.json"

response=$(curl -s -o /dev/null -w "%{http_code}" $ENDPOINT)

echo $response
if [ $response -lt 400 ]; then
    java -jar openapi-generator-cli.jar generate -i $ENDPOINT -g typescript -o api_client
    echo "all good"
else
    echo "The openapi schema is not reachable, are you sure the server is running?"
    exit 1
fi
