#!/bin/bash

KAFKA_CONNECT_ADDRESS=${1:-localhost}
KAFKA_CONNECT_PORT=${2:-8083}
BASE_CONFIG=${3:-"$(dirname $0)/elastic-sink-corporates.json"}
BASE_CONFIG2=${3:-"$(dirname $0)/elastic-sink-trades.json"}
KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

data=$(cat $BASE_CONFIG | jq -s '.[0]')
data2=$(cat $BASE_CONFIG2 | jq -s '.[0]')
curl -X POST $KAFKA_CONNECT_API --data "$data" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data2" -H "content-type:application/json"