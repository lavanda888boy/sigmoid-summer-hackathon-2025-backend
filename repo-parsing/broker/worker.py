import json
from message_broker import get_rabbitmq_channel


def callback(ch, method, properties, body):
  try:
    repo_info = json.loads(body.decode('utf-8'))
    print(f"✅ Received repo: {repo_info['name']} from {repo_info['owner']}")
  except Exception as e:
    print(f"❌ Failed to process message: {e}")
  finally:
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
  connection, channel = get_rabbitmq_channel(queue_name='repos')
  channel.basic_qos(prefetch_count=1)

  channel.basic_consume(queue='repos', on_message_callback=callback)
  channel.start_consuming()


if __name__ == "__main__":
  start_consumer()
