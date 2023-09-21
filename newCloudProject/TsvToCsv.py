import csv
import pika

class TsvToCsvComponent:
    def __init__(self, input_queue, output_queue):
        self.input_queue = input_queue
        self.output_queue = output_queue

    def run(self):
        while True:
            message = self.input_queue.receive()
            tsv_file_path = message["file_path"]

            # Convert the TSV file to a CSV file
            csv_file_path = "temp.csv"
            with open(csv_file_path, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                with open(tsv_file_path, "r") as tsv_file:
                    tsv_reader = csv.reader(tsv_file, delimiter="\t")
                    for row in tsv_reader:
                        csv_writer.writerow(row)

            # Publish the CSV file to the output queue
            self.output_queue.send(csv_file_path)

if __name__ == "__main__":
    # Connect to the message queue
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare the input and output queues
    input_queue = channel.queue_declare(queue="tsv_to_csv_input_queue")
    output_queue = channel.queue_declare(queue="tsv_to_csv_output_queue")

    # Create the TsvToCsv component
    tsv_to_csv_component = TsvToCsvComponent(input_queue, output_queue)

    # Start the TsvToCsv component
    tsv_to_csv_component.run()