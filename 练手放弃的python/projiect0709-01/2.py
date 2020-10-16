import pika
import time
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.0.169'))
channel = connection.channel()
channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(body)
    time.sleep(body.count(b'.'))
    print('Done')

channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()