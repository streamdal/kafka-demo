import kafka
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def consume(topic,kafka_url,bucket,org):
  consumer = kafka.KafkaConsumer(topic, bootstrap_servers=kafka_url, auto_offset_reset='earliest', enable_auto_commit=True, group_id='batch-consumer')
 
  for msg in consumer:
    message=json.loads(msg.value.decode('utf-8'))
    if "venue" in message and "group_state" in message["group"]:
      if message["group"]["group_state"] != "CA":
        if message["response"] == "yes":
          response=1
        else:
          response=0
        data = "event,group_id=%d,event_id='%s',group_state='%s' response=%d"  % (message["group"]["group_id"], message["event"]["event_id"], message["group"]["group_state"], response)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, data)

       

def influx_connect(token, url):
  client = InfluxDBClient(url=url, token=token)
  return client


#Influx
url="http://127.0.0.1:8086"
token="changeme"

#Kafka
topic='rsvps'
kafka_url=['127.0.0.1:9092']
org = "batch"
bucket = "rsvp"


#functions
client=influx_connect(token, url)
data=consume(topic, kafka_url, bucket, org)
