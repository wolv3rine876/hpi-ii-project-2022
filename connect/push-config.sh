#!/bin/bash

KAFKA_CONNECT_ADDRESS=${1:-localhost}
KAFKA_CONNECT_PORT=${2:-8083}
BASE_CONFIG1=${3:-"$(dirname $0)/elastic-sink-trades.json"}
BASE_CONFIG2=${3:-"$(dirname $0)/elastic-sink-rb_announcements.json"}
BASE_CONFIG3=${3:-"$(dirname $0)/elastic-sink-corporates.json"}
BASE_CONFIG4=${3:-"$(dirname $0)/elastic-sink-persons.json"}
BASE_CONFIG5=${3:-"$(dirname $0)/elastic-sink-trades-companies.json"}
KAFKA_CONNECT_API="$KAFKA_CONNECT_ADDRESS:$KAFKA_CONNECT_PORT/connectors"

data1=$(cat $BASE_CONFIG1 | jq -s '.[0]')
data2=$(cat $BASE_CONFIG2 | jq -s '.[0]')
data3=$(cat $BASE_CONFIG3 | jq -s '.[0]')
data4=$(cat $BASE_CONFIG4 | jq -s '.[0]')
data5=$(cat $BASE_CONFIG5 | jq -s '.[0]')

curl -X POST $KAFKA_CONNECT_API --data "$data1" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data2" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data3" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data4" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data5" -H "content-type:application/json"