#!/bin/bash

rm -f trade-companies.json;
rm -f trade-corporations.json;
rm -f trade-events.json;
rm -f trade-persons.json;

elasticdump --input=http://localhost:9200/trade-companies --output=trade-companies.json --type=data;
elasticdump --input=http://localhost:9200/trade-corporations --output=trade-corporations.json --type=data;
elasticdump --input=http://localhost:9200/trade-events --output=trade-events.json --type=data;
elasticdump --input=http://localhost:9200/trade-persons --output=trade-persons.json --type=data;