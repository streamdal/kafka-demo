import kafka
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def consume(topic,kafka_url):
  consumer = kafka.KafkaConsumer(topic, bootstrap_servers=kafka_url, auto_offset_reset='earliest', enable_auto_commit=True, group_id='batch-consumer')
 
  ## Influx settings

  token = "bNCydUmEkAkxtW-dmtfc6WRJnRXSRiZapkAqlii3xQtQBrULO1bwPr7OlgkCpmJdDcE1p38NcjB0fRiDMSiX8Q=="
  org = "batch"
  bucket = "rsvp"
  client = InfluxDBClient(url="http://127.0.0.1:8086", token=token)

  for msg in consumer:
    message=json.loads(msg.value.decode('utf-8'))
    if "venue" in message and "group_state" in message["group"]:
      if message["group"]["group_state"] != "CA":
        print("group_name: %s response: %s group_state: %s group_id: %d" % (message["group"]["group_name"], message["response"],message["group"]["group_state"], message["group"]["group_id"]))
        if message["response"] == "yes":
          response=1
        else:
          response=0
        data = "event,group_id=%d,event_id='%s',group_state='%s' response=%d"  % (message["group"]["group_id"], message["event"]["event_id"], message["group"]["group_state"], response)
        #data='event,group_name="Newgroup\ \Test",group_state="on" group_id=1,response=0' 
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, data)
      
topic='rsvps'
kafka_url=['127.0.0.1:9092']

consume(topic, kafka_url)
#write_topics(kafka_url, topic)
