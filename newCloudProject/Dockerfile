# Use an official Python runtime as base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Install Grafterizer (Replace this line with the actual installation command if it's different)
RUN wget "/path/to/grafterizer/url" && chmod +x "/path/to/grafterizer/executable"

# Install ArangoDB client if required (Replace this line with the actual installation if it's different)
RUN wget "/path/to/arango/url" && chmod +x "/path/to/arango/executable"

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run all the Python scripts
CMD ["sh", "-c", "python Arango.py && python Split.py && python Transform.py && python TsvToCsv.py && python Unzip.py"]