# Use the official NiceGUI image as the base image
FROM amd64/python:3.13-slim

# Set environment variables
ARG DOTENV_KEY
ENV DOTENV_KEY=$DOTENV_KEY

# Set working directory
WORKDIR /app

# Copy the application code to the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY /app .

# Make port 80 available to the world outside this container
EXPOSE 80

# Set the default command to run the NiceGUI app
CMD ["python3", "main.py"]
