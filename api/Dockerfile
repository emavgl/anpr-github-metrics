FROM python:3.6-slim
MAINTAINER emavgl

RUN apt-get update && apt-get install -y python3-dev

# Create app folder
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy requirements only and do pip install
# Good to do it here, so that when requirements stays the same, we don't run pip again
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . /usr/src/app

# Defaults for running
EXPOSE 5000
ENV FLASK_APP=run.py

RUN chmod +x ./init_script.sh
CMD ./init_script.sh
