#!/bin/bash
set -ex

GENERATOR_PATH=/home/ec2-user/kafka_load_generator/json-data-generator-1.2.2-SNAPSHOT
sed -i -e "s/\"broker.server\": .*,/\"broker.server\": \"$BROKER_IP\",/g" $GENERATOR_PATH/conf/cpuUsageConfig_firstCluster.json

CMD="java -jar -Xmx512m $GENERATOR_PATH/json-data-generator-1.2.2-SNAPSHOT.jar cpuUsageConfig_firstCluster.json"
for run in {1..30}
  do $CMD > /dev/null  2&>1 &
done
