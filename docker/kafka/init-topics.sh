#!/bin/bash

set -e

BOOTSTRAP_SERVER="kafka:9094"

echo "Waiting for Kafka to become available..."

until /opt/kafka/bin/kafka-topics.sh \
    --bootstrap-server ${BOOTSTRAP_SERVER} \
    --list >/dev/null 2>&1
do
    sleep 2
done

echo "Kafka is ready."

TOPICS=(
    "perflens.metrics"
)

for topic in "${TOPICS[@]}"
do

    echo "Creating topic: ${topic}"

    /opt/kafka/bin/kafka-topics.sh \
        --bootstrap-server ${BOOTSTRAP_SERVER} \
        --create \
        --if-not-exists \
        --topic "${topic}" \
        --partitions 3 \
        --replication-factor 1

done

echo "Kafka topic initialization complete."