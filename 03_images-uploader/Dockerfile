FROM python:2.7.10
MAINTAINER Tomasz Skibinski <tomasz.skibinski@linxsys.pl>

RUN apt-get update -yq \
    && apt-get install -qq -y libmysqlclient-dev

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY images_uploader.py /iUploader/images_uploader
COPY config.py /iUploader/config.py
COPY templates /iUploader/templates

RUN apt-get clean -qy \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

ENTRYPOINT [ "/usr/local/bin/python" ]
CMD [ "/iUploader/images_uploader" ]
