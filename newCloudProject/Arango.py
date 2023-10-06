import arangodb
import json
import pika

class ArangoComponent:
    def __init__(self, input_queue, database_name, collection_name, grafterizer_transformation_json_path):
        self.input_queue = input_queue
        self.database_name = database_name
        self.collection_name = collection_name
        self.grafterizer_transformation_json_path = grafterizer_transformation_json_path

        # Connect to ArangoDB
        self.client = arangodb.ArangoDBClient()
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def run(self):
        while True:
            message = self.input_queue.receive()
            csv_file_path = message["output_csv_file_path"]

            # Load the Grafterizer transformation JSON
            with open(self.grafterizer_transformation_json_path, "r") as f:
                transformation_json = json.load(f)

            # Convert the CSV file to ArangoDB documents
            with open(csv_file_path, "r") as f:
                for line in f:
                    # Split the CSV line into fields
                    fields = line.strip().split(",")

                    # Create an ArangoDB documentg
                    document = {}
                    for i in range(len(fields)):
                        document[transformation_json["fields"][i]] = fields[i]

                    print("\n ArangoDB document created \n")

                    # Insert the document into ArangoDB
                    self.collection.insert(document)

if __name__ == "__main__":
    # Connect to the message queue
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare the input queue
    input_queue = channel.queue_declare(queue="transform_queue")

    # Create the Arango component
    arango_component = ArangoComponent(input_queue, database_name="my_database", collection_name="my_collection", grafterizer_transformation_json_path="/path/to/grafterizer/transformation.json")

    # Start the Arango component
    arango_component.run()