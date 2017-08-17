#!/bin/bash
MY_IP="$(ifconfig | grep -A 1 'eth0' | tail -1 | cut -d ':' -f 2 | cut -d ' ' -f 1)"

if [[ -n `grep "10.*localhost" /etc/hosts` ]]; then
  sed -i "s/^10.*localhost$/$MY_IP `hostname` localhost/" /etc/hosts
else
  echo "$MY_IP `hostname` localhost" >> /etc/hosts
fi

mv /home/ec2-user/kafka_2.11-0.11.0.0 /root/
JMX_PATH="/root/consumer/"
KAFKA_PATH="/root/kafka_2.11-0.11.0.0/"
JMX_PORT=44444 $KAFKA_PATH/bin/kafka-console-consumer.sh --bootstrap-server $BROKER_IP:9092 --topic cpu-usage > /dev/null 2>&1 &
cd $JMX_PATH
JMXTRANS_OPTS="-Dport1=44444 -Durl1=localhost -DinfluxUrl=http://10.0.0.83:8086/ -DinfluxDb=kafka -DinfluxUser=admin -DinfluxPwd=admin" SECONDS_BETWEEN_RUNS=15 JAR_FILE=jmxtrans-259-all.jar ./jmxtrans.sh start
