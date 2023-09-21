#!/usr/bin/env python
import pika

# defining what to do when a message is received
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    # declaring the queue again (to be sure)
    channel.queue_declare(queue='hello')
    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)
    # wait for messages
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

    print('**** After start consuming')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
