FROM python:3.7.9-buster

LABEL maintainer="juanernestobiondi@gmail.com"

# Define environment variable
# If you are behind a proxy uncomment and edit lines below
# ENV http_proxy "http://<USER>:<PASSWORD>@<IP>:<PORT>"
# ENV https_proxy "http://<USER>:<PASSWORD>@<IP>:<PORT>"

# Copy application files.
COPY . /app

# Setup working directory.
WORKDIR /app

# Update the system and install needed packages
RUN apt-get update && \
   apt-get upgrade -y && \
   apt-get install --yes git && \
   pip3 install -r ./requirements.txt

# Expose port 8080 for the Flask app to run on
EXPOSE 8080

# Delete all the apt list files since they're big and get stale quickly
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set default language to English
ENV LANG en

# Execute the application
CMD ["python3", "run.py"]
