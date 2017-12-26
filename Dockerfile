FROM python:latest

ENV PROJECT=/fileuploader
ENV ROOT_DIRECTORY=$PROJECT/rootdir

WORKDIR /fileuploader

ADD . /fileuploader

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 5000

VOLUME ${PROJECT}
VOLUME ${ROOT_DIRECTORY}

ENV FLASK_APP ./app/entry.py
ENV FLASK_DEBUG 0

CMD ["entry.py"]