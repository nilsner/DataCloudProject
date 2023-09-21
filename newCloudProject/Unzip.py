import zipfile
import csv
import pika

class UnzipComponent:
    def __init__(self, output_queue):
        self.output_queue = output_queue

    def run(self):
        while True:
            zip_file_path = "file_path"

            # Extract the TSV file from the zip file
            with zipfile.ZipFile(zip_file_path, "r") as zip_file:
                zip_file_member = zip_file.namelist()[0]
                with zip_file.open(zip_file_member) as zip_file_member:
                    tsv_data = zip_file_member.read()

            # Publish the UnzipTsv file to the output queue
            self.output_queue.send(tsv_data)

if __name__ == "__main__":
    # Connect to the message queue
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare the input and output queues
    output_queue = channel.queue_declare(queue="unzip_output_queue")

    # Create the Unzip component
    unzip_component = UnzipComponent(output_queue)

    # Start the Unzip component
    unzip_component.run()