#!/bin/bash

rm -f rb-announcements.json;
rm -f trade-companies.json
rm -f trade-events.json
rm -f persons.json
rm -f corporates.json

# trades
elasticdump --input=http://localhost:9200/trade-companies --output=trade-companies.json --type=data;
elasticdump --input=http://localhost:9200/trade-events --output=trade-events.json --type=data;
# rb
elasticdump --input=http://localhost:9200/rb-announcements --output=rb-announcements.json --type=data;
# persons
elasticdump --input=http://localhost:9200/persons --output=persons.json --type=data;
# corporates
elasticdump --input=http://localhost:9200/corporates --output=corporates.json --type=data;