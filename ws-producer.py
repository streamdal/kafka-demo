import kafka 
import websocket

def write_topics(hsb_url, topic):
  topic_list = []
  kafka_client = kafka.KafkaAdminClient(bootstrap_servers=hsb_url, client_id='populate')
  if topic not in kafka_client.list_topics():
    topic_list.append(kafka.admin.NewTopic(name=topic, num_partitions=5, replication_factor=1))     
    kafka_client.create_topics(new_topics=topic_list, validate_only=False)


def on_message(wsapp, message):
    producer = kafka.KafkaProducer(bootstrap_servers='127.0.0.1:9092', client_id='producer')
    producer.send('rsvps', message.encode('utf-8'))

topic='rsvps'
kafka_url="127.0.0.1:9092"

write_topics(kafka_url, topic)
wsapp = websocket.WebSocketApp("wss://stream.meetup.com/2/rsvps", on_message=on_message)
wsapp.run_forever()
