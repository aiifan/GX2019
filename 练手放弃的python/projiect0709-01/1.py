import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.169'))
channel = connection.channel()
channel.queue_declare(queue='hello')
message = ''.join(sys.argv[1:] or 'Hello World')
channel.basic_publish(exchange='', routing_key='hello', body=message)
print("[x] Sent %r" % message)
connection.close()