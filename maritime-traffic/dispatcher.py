

#!/usr/bin/env python
import pika
import json

# defining what to do when a message is received
def callback(ch, method, properties, body):

    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    body_str = body.decode('utf8').replace("'", '"')
    body_json = json.loads(body_str)

    if body_json["boat_speed"] > 5 :
        # send the message to Speed estimator, through the exchange ''
        # which simply delivers to the queue having the key as name
        ch.basic_publish(exchange='',
                         routing_key='kns-tc_at_sea_stream',
                         body=str(body_str))

        print(" [x] Sent: " + str(body_str))
    else :
        # send the message to Classifier, through the exchange ''
        # which simply delivers to the queue having the key as name
        ch.basic_publish(exchange='',
                         routing_key='kns-tc_at_port_stream',
                         body=str(body_str))
        
        print(" [x] Sent: " + str(body_str))

   


def main():
    credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='kns-tc_boat_stream')
    channel.queue_declare(queue='kns-tc_at_port_stream')
    channel.queue_declare(queue='kns-tc_at_sea_stream')
    

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='kns-tc_boat_stream',
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
