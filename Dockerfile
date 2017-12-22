FROM python:latest

ENV PROJECT = /fileuploader

WORKDIR /fileuploader

ADD . /fileuploader

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

VOLUME ${PROJECT}

ENV FLASK_APP entry.py
ENV FLASK_DEBUG 0

CMD ["entry.py"]