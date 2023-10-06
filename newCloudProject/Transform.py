import subprocess
import pika

class TransformComponent:
    def __init__(self, input_queue, output_queue, grafterizer_executable_path):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.grafterizer_executable_path = grafterizer_executable_path

    def run(self):
        while True:
            message = self.input_queue.receive()
            csv_file_path = message["file_path"]

            # Clean and preprocess the CSV file using Grafterizer
            output_csv_file_path = "temp.csv"
            subprocess.run([self.grafterizer_executable_path, csv_file_path, output_csv_file_path])

            # Publish the output CSV file to the message queue
            self.output_queue.send(output_csv_file_path)

if __name__ == "__main__":
    # Connect to the message queue
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare the input and output queues
    input_queue = channel.queue_declare(queue="split_csv_queue")
    output_queue = channel.queue_declare(queue="transform_queue")

    # Create the Transform component
    transform_component = TransformComponent(input_queue, output_queue, grafterizer_executable_path="/path/to/grafterizer/executable")

    # Start the Transform component
    transform_component.run()