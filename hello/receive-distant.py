#!/usr/bin/env python
import pika

# defining what to do when a message is received
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def main():
    #getting a connection to the broker
    credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring the queue again (to be sure)
    channel.queue_declare(queue='hellokarthika')

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='hellokarthika',
                      auto_ack=True,
                      on_message_callback=callback)
    # wait for messages
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
