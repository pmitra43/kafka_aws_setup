#!/bin/bash
echo "127.0.0.1  `hostname`" >> /etc/hosts
mv /home/ec2-user/kafka_2.11-0.11.0.0 /root/
JMX_PATH="/root/consumer/"
KAFKA_PATH="/root/kafka_2.11-0.11.0.0/"
JMXTRANS_OPTS="-Dport1=44444 -Durl1=localhost -DinfluxUrl=http://10.0.0.83:8086/ -DinfluxDb=kafka -DinfluxUser=admin -DinfluxPwd=admin" SECONDS_BETWEEN_RUNS=15 JAR_FILE=$JMX_PATH/jmxtrans-259-all.jar $JMX_PATH/jmxtrans.sh start
JMX_PORT=44444 $KAFKA_PATH/bin/kafka-console-consumer.sh --bootstrap-server $BROKER_IP:9092 --topic cpu-usage > /dev/null 2>&1 &
