import os

import zipfile
import csv
import pika

class UnzipComponent:
    def __init__(self, output_queue):
        self.output_queue = output_queue

    def run(self):
        while True:
            #zip_file_path = "file_path"

            file_path = "/path/to/data.zip"  # Replace with the actual file path on the shared file system
            output_dir = "/path/to/output/directory"
            # Assuming file_path is a valid path to a .zip file on a shared file system
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                for filename in zip_ref.namelist():
                    if filename.endswith('.tsv'):
                        destination_path = os.path.join(output_dir, filename)
                        zip_ref.extract(filename, output_dir)
                        print(f" [x] Extracted {filename} to {destination_path}")

            # Publish the UnzipTsv file to the output queue
            self.output_queue.send(destination_path)

if __name__ == "__main__":
    # Connect to the message queue
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare the input and output queues
    output_queue = channel.queue_declare(queue="unzip_tsv_queue")

    # Create the Unzip component
    unzip_component = UnzipComponent(output_queue)

    # Start the Unzip component
    unzip_component.run()