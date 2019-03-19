# Ubuntu 18.04
FROM ubuntu:18.04

LABEL maintainer="juanernestobiondi@gmail.com"

# Update the system
RUN apt-get update && apt-get upgrade -y

# Install Python related
RUN apt-get install -y python3 python3-dev python3-pip

# Install SQLite3
RUN apt-get install --yes --force-yes sqlite3

# Copy files over the container
COPY ./ ./thing_organizer_app

# Set working directory
WORKDIR ./thing_organizer_app

# Install pip requirements
RUN pip3 install -r requirements.txt

# unblock port 8080 for the Flask app to run on
EXPOSE 8080

# Delete all the apt list files since they're big and get stale quickly
# RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set default language to English
ENV LANG en

# Execute the application
CMD ["python3", "run_app.py", "run_development"]
