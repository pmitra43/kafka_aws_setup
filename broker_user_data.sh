#!/bin/bash
set -ex
MY_IP="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"

if [[ -n `grep "10.*localhost" /etc/hosts` ]]; then
  sed -i "s/^10.*localhost$/$MY_IP `hostname` localhost/" /etc/hosts
else
  echo "$MY_IP `hostname` localhost" >> /etc/hosts
fi

JMX_PATH="/root/broker"
KAFKA_PATH="/root/kafka_2.11-0.11.0.0"

sed -i "s/#*listeners=PLAINTEXT:\/\/.*:9092/listeners=PLAINTEXT:\/\/$MY_IP:9092/" $KAFKA_PATH/config/server.properties
sed -i 's/zookeeper.connect=.*/zookeeper.connect=$ZOOKEEPER_IP:2181/' $KAFKA_PATH/config/server.properties

JMX_PORT=55555 $KAFKA_PATH/bin/kafka-server-start.sh $KAFKA_PATH/config/server.properties > $KAFKA_PATH/broker_log.log &
sleep 1m
cd $JMX_PATH
JMXTRANS_OPTS="-Dport1=55555 -Durl1=localhost -DinfluxUrl=http://10.0.0.83:8086/ -DinfluxDb=kafka -DinfluxUser=admin -DinfluxPwd=admin" JAR_FILE=jmxtrans-259-all.jar ./jmxtrans.sh start
