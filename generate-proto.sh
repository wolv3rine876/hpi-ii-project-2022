#!/bin/bash

protoc --proto_path=proto --python_out=build/gen proto/bakdata/corporate/v1/corporate.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/corporate/v1/announcement.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/corporate/v1/person.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/trade/v1/trade.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/trade/v1/person.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/trade/v1/corporation.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/trade/v1/company.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/dedup/v1/person.proto
protoc --proto_path=proto --python_out=build/gen proto/bakdata/dedup/v1/corporate.proto