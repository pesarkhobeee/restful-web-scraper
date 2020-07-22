From python:3.8
MAINTAINER Farid Ahmadian "ahmadian.farid.1988@gmail.com"
RUN apt-get update -y && \
    apt-get install -y python-pip

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn" ]
CMD [ "-w", "4", "-b", "0.0.0.0:8080", "api:app"]
