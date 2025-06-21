from dotenv import load_dotenv
import os
import pika
import ssl


load_dotenv()
context = ssl.create_default_context()

def get_rabbitmq_channel(queue_name='repos'):
  credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASS"))

  parameters = pika.ConnectionParameters(
    host=os.getenv("RABBITMQ_HOST"),
    port=os.getenv("RABBITMQ_PORT"),
    credentials=credentials,
    ssl_options=pika.SSLOptions(context)
  )

  connection = pika.BlockingConnection(parameters)
  channel = connection.channel()
  channel.queue_declare(queue=queue_name)

  return connection, channel