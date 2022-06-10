#!/bin/bash

rm -f rb-persons.json;
rm -f rb-announcements.json;
rm -f rb-corporates.json;

elasticdump --input=http://localhost:9200/rb-persons --output=rb-persons.json --type=data;
elasticdump --input=http://localhost:9200/rb-announcements --output=rb-announcements.json --type=data;
elasticdump --input=http://localhost:9200/rb-corporates --output=rb-corporates.json --type=data;