

#!/usr/bin/env python
import pika
import json



ports = [0] * 5
# defining what to do when a message is received
def callback(ch, method, properties, body):
    global ports
    print(" [x] Received %r" % body)

    # decoding bytes into string and formatting into JSON
    body_str = body.decode('utf8').replace("'", '"')
    body_json = json.loads(body_str)

    port = (body_json["boat_destination"])
    if(port == "BREST"):
        ports[0]+=1
    elif(port == "VALENCIA"):
        ports[1]+=1
    elif(port == "PALERMO"):
        ports[2]+=1
    elif(port == "BRIGHTON"):
        ports[3]+=1
    elif(port == "AMSTERDAM"):
        ports[4]+=1
 

    print(ports)


def main():
    credentials = pika.PlainCredentials('zprojet', 'rabbit22')
    parameters = pika.ConnectionParameters('rabbitmqserver', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # declaring input and output queues
    channel.queue_declare(queue='kns-tc_at_port_stream')

    # auto_ack: as soon as collected, a message is considered as acked
    channel.basic_consume(queue='kns-tc_at_port_stream',
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
