

#!/usr/bin/env python
import pika
import json

nb_boats = 0
sum_of_speed = 0

# defining what to do when a message is received
def callback(ch, method, properties, body):
    global sum_of_speed
    global nb_boats
    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    body_str = body.decode('utf8').replace("'", '"')
    body_json = json.loads(body_str)

    sum_of_speed += body_json["boat_speed"]
    nb_boats += 1
    avg =  sum_of_speed / nb_boats 

    print(" [x] Average speed : %f" %avg)


def main():
    global sum_of_speed
    global nb_boats
    nb_boats = 0
    sum_of_speed = 0
    
    credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='kns-tc_at_sea_stream')

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='kns-tc_at_sea_stream',
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
