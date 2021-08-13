#!/bin/bash
#
# Simple start script
#
PLUMBER_RELAY_TYPE=kafka \
PLUMBER_RELAY_TOKEN=changme \
PLUMBER_RELAY_GRPC_ADDRESS=grpc-collector.batch.sh:9000 \
PLUMBER_RELAY_KAFKA_ADDRESS=127.0.0.1:9092 \
PLUMBER_RELAY_KAFKA_TOPIC=rsvps \
PLUMBER_RELAY_KAFKA_GROUP_ID=Batch \
PLUMBER_RELAY_KAFKA_USE_CONSUMER_GROUP=true \
plumber relay --listen-address=":8081" --stats
