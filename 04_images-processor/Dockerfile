FROM python:2.7.10
MAINTAINER Tomasz Skibinski <tomasz.skibinski@linxsys.pl>

RUN apt-get update -yq \
    && apt-get install -qq -y libmysqlclient-dev imagemagick ghostscript

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY images_processor.py /iProcessor/images_processor
COPY config.py /iProcessor/config.py

RUN apt-get clean -qy \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/*

ENTRYPOINT [ "/usr/local/bin/python" ]
CMD [ "/iProcessor/images_processor" ]
