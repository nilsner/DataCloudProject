import csv
import pika
import os

class SplitComponent:
    def __init__(self, input_queue, output_queue, max_rows_per_file):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.max_rows_per_file = max_rows_per_file

    def run(self):
        while True:
            message = self.input_queue.receive()
            csv_file_path = message["file_path"]

            # Get the size of the CSV file
            csv_file_size = os.path.getsize(csv_file_path)

            # Calculate the number of files to split the CSV file into
            num_files = csv_file_size // self.max_rows_per_file + 1

            # Create a new directory to store the split CSV files
            output_directory = "/path/to/your/split_files/directory"
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            # Split the CSV file into smaller pieces
            for i in range(num_files):
                output_csv_file_path = os.path.join(output_directory,f"output_{i}.csv")
                with open(output_csv_file_path, "w") as output_csv_file:
                    csv_writer = csv.writer(output_csv_file, delimiter=",")
                    with open(csv_file_path, "r") as input_csv_file:
                        csv_reader = csv.reader(input_csv_file, delimiter=",")
                        for row in csv_reader:
                            csv_writer.writerow(row)

                # Publish the output CSV file to the message queue
                self.output_queue.send(output_directory)

if __name__ == "__main__":
    # Connect to the message queue
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare the input and output queues
    input_queue = channel.queue_declare(queue="csv_queue")
    output_queue = channel.queue_declare(queue="split_csv_queue")

    # Create the Split component
    split_component = SplitComponent(input_queue, output_queue, max_rows_per_file=100000) # 100,000 rows per file

    # Start the Split component
    split_component.run()