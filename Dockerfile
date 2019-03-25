# Ubuntu 18.04
FROM ubuntu:18.04

LABEL maintainer="juanernestobiondi@gmail.com"

# Define environment variable
# If you are behind a proxy uncomment and edit lines below
# ENV http_proxy "http://<USER>:<PASSWORD>@<IP>:<PORT>"
# ENV https_proxy "http://<USER>:<PASSWORD>@<IP>:<PORT>"

# Update the system
RUN apt-get update && apt-get upgrade -y

# Install SQLite3
RUN apt-get install --yes --force-yes sqlite3

# Install Python related
RUN apt-get install -y git python3 python3-dev python3-pip

# Copy files over the container
RUN git clone https://github.com/yeyeto2788/Things-Organizer.git

# Make all files writables
RUN chmod -R 777 ./Things-Organizer

# Move into clone repository
RUN cd ./Things-Organizer

# Set working directory
WORKDIR ./Things-Organizer

# Install pip requirements
# If you're behind proxy uncomment and edit line below.
# RUN pip3 install --proxy http://<IP>:<PORT> -r requirements.txt
# Otherwise leave it as is
RUN pip3 install -r requirements.txt

# unblock port 8080 for the Flask app to run on
EXPOSE 8080

# Delete all the apt list files since they're big and get stale quickly
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set default language to English
ENV LANG en

# Execute the application
CMD ["python3", "run_app.py", "create_db"]
CMD ["python3", "run_app.py", "run_production"]
