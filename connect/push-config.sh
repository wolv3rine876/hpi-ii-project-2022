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

data=$(cat $BASE_CONFIG | jq -s '.[0]')
data2=$(cat $BASE_CONFIG2 | jq -s '.[0]')
data3=$(cat $BASE_CONFIG3 | jq -s '.[0]')
data4=$(cat $BASE_CONFIG4 | jq -s '.[0]')
data5=$(cat $BASE_CONFIG5 | jq -s '.[0]')
<<<<<<< HEAD

=======
>>>>>>> e92c3762998bbe7957ce764d678b4f3fe875da67
curl -X POST $KAFKA_CONNECT_API --data "$data" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data2" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data3" -H "content-type:application/json"
curl -X POST $KAFKA_CONNECT_API --data "$data4" -H "content-type:application/json"
<<<<<<< HEAD
curl -X POST $KAFKA_CONNECT_API --data "$data5" -H "content-type:application/json"
=======
curl -X POST $KAFKA_CONNECT_API --data "$data5" -H "content-type:application/json"
>>>>>>> e92c3762998bbe7957ce764d678b4f3fe875da67
