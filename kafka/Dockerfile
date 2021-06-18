FROM ubuntu

RUN apt update && apt install -y nano openjdk-8-jre wget 

RUN wget https://downloads.apache.org/kafka/2.8.0/kafka_2.13-2.8.0.tgz

RUN tar -xzf kafka_2.13-2.8.0.tgz
CMD kafka_2.13-2.8.0/bin/kafka-server-start.sh kafka_2.13-2.8.0/config/server.properties
CMD kafka_2.13-2.8.0/bin/kafka-topics.sh --create --topic test --bootstrap-server localhost:9092