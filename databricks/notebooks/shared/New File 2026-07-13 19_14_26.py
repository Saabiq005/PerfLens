# """
# Kafka reader for PerfLens Bronze ingestion.
# """

# from shared.config import (
#     EVENTHUB_CONNECTION_STRING,
#     KAFKA_BOOTSTRAP_SERVERS,
#     TOPIC,
# )

EVENTHUB_CONNECTION_STRING = "<your_eventhub_connection_string>"
KAFKA_BOOTSTRAP_SERVERS = "<your_kafka_bootstrap_servers>"
TOPIC = "<your_topic>"

class KafkaReader:

    @staticmethod
    def create_stream(spark):

        kafka_options = {

            "kafka.bootstrap.servers":
                KAFKA_BOOTSTRAP_SERVERS,

            "subscribe":
                TOPIC,

            "startingOffsets":
                "latest",

            "kafka.security.protocol":
                "SASL_SSL",

            "kafka.sasl.mechanism":
                "PLAIN",

            "kafka.sasl.jaas.config":
                (
                    "org.apache.kafka.common.security.plain."
                    "PlainLoginModule required "
                    'username="$ConnectionString" '
                    f'password="{EVENTHUB_CONNECTION_STRING}";'
                )
        }

        return (
            spark.readStream
                 .format("kafka")
                 .options(**kafka_options)
                 .load()
        )