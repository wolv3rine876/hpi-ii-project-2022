#!/bin/bash

KAFKA_CONNECT_ADDRESS=${1:-localhost}
KAFKA_CONNECT_PORT=${2:-8083}
BASE_CONFIG=${3:-"$(dirname $0)/elastic-sink-corporates.json"}
BASE_CONFIG2=${3:-"$(dirname $0)/elastic-sink-trades.json"}
<<<<<<< HEAD
BASE_CONFIG3=${3:-"$(dirname $0)/elastic-sink-rb_announcements.json"}
BASE_CONFIG4=${3:-"$(dirname $0)/elastic-sink-rb_corporates.json"}
BASE_CONFIG5=${3:-"$(dirname $0)/elastic-sink-rb_persons.json"}
=======
BASE_CONFIG3=${3:-"$(dirname $0)/elastic-sink-trades-persons.json"}
BASE_CONFIG4=${3:-"$(dirname $0)/elastic-sink-trades-corporations.json"}
BASE_CONFIG5=${3:-"$(dirname $0)/elastic-sink-trades-companies.json"}
>>>>>>> e92c3762998bbe7957ce764d678b4f3fe875da67
KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

CONNECTOR_NAME=$(jq -r .name $BASE_CONFIG)
CONNECTOR_NAME2=$(jq -r .name $BASE_CONFIG2)
CONNECTOR_NAME3=$(jq -r .name $BASE_CONFIG3)
CONNECTOR_NAME4=$(jq -r .name $BASE_CONFIG4)
CONNECTOR_NAME5=$(jq -r .name $BASE_CONFIG5)
curl -Is -X DELETE $KAFKA_CONNECT_API/$CONNECTOR_NAME
curl -Is -X DELETE $KAFKA_CONNECT_API/$CONNECTOR_NAME2
curl -Is -X DELETE $KAFKA_CONNECT_API/$CONNECTOR_NAME3
curl -Is -X DELETE $KAFKA_CONNECT_API/$CONNECTOR_NAME4
curl -Is -X DELETE $KAFKA_CONNECT_API/$CONNECTOR_NAME5
