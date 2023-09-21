#!/usr/bin/env python
import pika

# getting a connection to the broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# declaring the queue
channel.queue_declare(queue='CVS')

# send the message, through the exchange ''
# which simply delivers to the queue having the key as name
channel.basic_publish(exchange='',
                      routing_key='cvs-file',
                      body='FILE GOES HERE!')
print(" [x] Sent to first message queue")

# gently close (flush)
connection.close()
