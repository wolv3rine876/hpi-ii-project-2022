# HPI information integration project SoSe 2022

This repository provides a code base for the information integration course in the summer semester of 2022. Below you
can find the documentation for setting up the project.

## Prerequisites

- Install [Poetry](https://python-poetry.org/docs/#installation)
- Install [Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/)
- Install [Protobuf compiler (protoc)](https://grpc.io/docs/protoc-installation/). If you are using windows you can
  use [this guide](https://www.geeksforgeeks.org/how-to-install-protocol-buffers-on-windows/)
- Install [jq](https://stedolan.github.io/jq/download/)

## Architecture
![](architecture.png)

### RB Website

The [Registerbekanntmachung website](https://www.handelsregisterbekanntmachungen.de/index.php?aktion=suche) contains
announcements concerning entries made into the companies, cooperatives, and
partnerships registers within the electronic information and communication system. You can search for the announcements.
Each announcement can be requested through the link below. You only need to pass the query parameters `rb_id`
and `land_abk`. For instance, we chose the state Rheinland-Pfalz `rp` with an announcement id of `56267`, the
new entry of the company BioNTech.

```shell
export STATE="rp" 
export RB_ID="56267"
curl -X GET  "https://www.handelsregisterbekanntmachungen.de/skripte/hrb.php?rb_id=$RB_ID&land_abk=$STATE"
```

### Trades Website

The [Eigengeschäfte von Führungskräften Database](https://portal.mvp.bafin.de/database/DealingsInfo/) contains information on managers who bought big
shares in a company and therefore had to notify the German BAFIN. Data can be retrieved by the issuer's first letter (e.g. Z for Zalando).

### Kafka Connect

[Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html) is a tool to move large data sets into
(source) and out (sink) of Kafka.
Here we only use the Sink connector, which consumes data from a Kafka topic into a secondary index such as
Elasticsearch.

We use the [Elasticsearch Sink Connector](https://docs.confluent.io/kafka-connect-elasticsearch/current/overview.html)
to move the data from the `coporate-events` and `trade-events` topics into the Elasticsearch.

## Setup

This project uses [ ](https://python-poetry.org/) as a build tool.
To install all the dependencies, just run `poetry install`.

This project uses Protobuf for serializing and deserializing objects. We provided a
simple [protobuf schema](./proto/bakdata/corporate/v1/corporate.proto).
Furthermore, you need to generate the Python code for the model class from the proto file.
To do so run the [`generate-proto.sh`](./generate-proto.sh) script.
This script uses the [Protobuf compiler (protoc)](https://grpc.io/docs/protoc-installation/) to generate two model classes
under the `build/gen/bakdata/corporate/v1` and `build/gen/bakdata/trades/v1` folder
with the name `corporate_pb2.py` and `trade_pb2.py`.

## Run

### Infrastructure

Use `docker-compose up -d` to start all the services: [Zookeeper](https://zookeeper.apache.org/)
, [Kafka](https://kafka.apache.org/), [Schema
Registry](https://docs.confluent.io/platform/current/schema-registry/index.html)
, [Kafka REST Proxy]((https://github.com/confluentinc/kafka-rest)), [Kowl](https://github.com/redpanda-data/kowl),
[Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html),
and [Elasticsearch](https://www.elastic.co/elasticsearch/). Depending on your system, it takes a couple of minutes
before the services are up and running. You can use a tool
like [lazydocker](https://github.com/jesseduffield/lazydocker)
to check the status of the services.

### Kafka Connect

After all the services are up and running, you need to configure Kafka Connect to use the Elasticsearch sink connector.
The config file is a JSON formatted file. We provided two [basic configuration file](./connect/elastic-sink-corporates.json) and [basic configuration file](./connect/elastic-sink-trades.json).
You can find more information about the configuration properties on
the [official documentation page](https://docs.confluent.io/kafka-connect-elasticsearch/current/overview.html).

To start the connector, you need to push the JSON config file to Kafka. You can either use the UI dashboard in Kowl or
use the [bash script provided](./connect/push-config.sh). It is possible to remove a connector by deleting it
through Kowl's UI dashboard or calling the deletion API in the [bash script provided](./connect/delete-config.sh).

### RB Crawler

You can start the rb_crawler with the command below:

```shell
poetry run python rb_crawler/main.py --id $RB_ID --state $STATE
```

The `--id` option is an integer, which determines the initial event in the handelsregisterbekanntmachungen to be
crawled.

The `--state` option takes a string (only the ones listed above). This string defines the state where the crawler should
start from.

You can use the `--help` option to see the usage:

```
Usage: main.py [OPTIONS]

Options:
  -i, --id INTEGER                The rb_id to initialize the crawl from
  -s, --state [bw|by|be|br|hb|hh|he|mv|ni|nw|rp|sl|sn|st|sh|th]
                                  The state ISO code
  --help                          Show this message and exit.
```

### Trades Crawler

You can start the trades crawler with the command below:

```shell
poetry run python trades_crawler/main.py
```

You can use the `--help` option to see the usage:

```
Usage: main.py [OPTIONS]

Options:
  -i, --issuer TEXT  The issuer's first letter to start with (e.g. 'B')
  --help             Show this message and exit.
```

### Dedup

You can start the deduplication with the commands below:

```shell
poetry run python dedup/main.py --topic_type corporates
```
```shell
poetry run python dedup/main.py --topic_type persons
```

You can use the `--help` option to see the usage:

```
Usage: main.py [OPTIONS]

Options:
  --topic_type TEXT  Enter the topic you want to run the deduplication on.
  --help             Show this message and exit.
```

### Architecture

The Architecture of the Trades crawler is the same as the RB Crawler excluding the schema. Thus, it is composed of a extractor that queries our source and a producer that communicates with Kafka. The Schema can be found in proto/bakdata/trade/v1/trade.proto.
Furthermore, the dedup component subscribes to all person and corporate topics and tries to filter out duplicates by introducing a dedup_id.

## Query data

### Kowl

[Kowl](https://github.com/redpanda-data/kowl) is a web application that helps you manage and debug your Kafka workloads
effortlessly. You can create, update, and delete Kafka resources like Topics and Kafka Connect configs.
You can see Kowl's dashboard in your browser under http://localhost:8080.

### Elasticsearch

To query the data from Elasticsearch, you can use
the [query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/query-dsl.html) of elastic. For example:

```shell
curl -X GET "localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match": {
            <field>
        }
    }
}
'
```

`<field>` is the field you wish to search. For example:

```
"reference_id":"HRB 41865"
```

```
"isin":"DE000ZAL1111"
```

```
"name":"rollmann"
```

```
"dedup_id" : "eadd6f2ba826df2cb5f3da0a71ee302a"
```

## Teardown
You can stop and remove all the resources by running:
```shell
docker-compose down
```