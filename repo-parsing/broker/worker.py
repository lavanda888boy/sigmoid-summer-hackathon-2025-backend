import json
import os
import requests
from message_broker import get_rabbitmq_channel


def send_repo_request(repo_info):
  url = "http://localhost:8000/repos/create/"
  
  headers = {
    os.getenv("WORKER_PASS_HEADER"): os.getenv("WORKER_PASS_VALUE"),
    "Content-Type": "application/json"
  }
  
  try:
    requests.post(url, json=repo_info, headers=headers)
  except requests.RequestException as e:
    print(f"Error: {e}")


def callback(ch, method, properties, body):
  try:
    repo_info = json.loads(body.decode('utf-8'))
    send_repo_request(repo_info)
  except Exception as e:
    print(f"❌ Failed to forward repo: {e}")
  finally:
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
  connection, channel = get_rabbitmq_channel(queue_name='repos')
  channel.basic_qos(prefetch_count=1)

  channel.basic_consume(queue='repos', on_message_callback=callback)
  channel.start_consuming()


if __name__ == "__main__":
  start_consumer()
