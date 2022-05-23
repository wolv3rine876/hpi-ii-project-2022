#!/bin/bash

KAFKA_CONNECT_ADDRESS=${1:-localhost}
KAFKA_CONNECT_PORT=${2:-8083}
BASE_CONFIG=${3:-"$(dirname $0)/elastic-sink-corporates.json"}
BASE_CONFIG2=${3:-"$(dirname $0)/elastic-sink-trades.json"}
KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

CONNECTOR_NAME=$(jq -r .name $BASE_CONFIG)
CONNECTOR_NAME2=$(jq -r .name $BASE_CONFIG2)
curl -Is -X DELETE $KAFKA_CONNECT_API/$CONNECTOR_NAME
curl -Is -X DELETE $KAFKA_CONNECT_API/$CONNECTOR_NAME2
