FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PLONE_VERSION 5.2.14

RUN apt-get update && apt-get install -y \n    gcc \n    build-essential \n    libssl-dev \n    libxml2-dev \n    libxslt1-dev \n    libz-dev \n    libjpeg-dev \n    libreadline-dev \n    wv \n    poppler-utils \n    wget \n    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash plone

# Use setuptools matching Plone 5.2.14 versions.cfg and a modern zc.buildout
RUN pip install --no-cache-dir "setuptools==65.7.0" "zc.buildout==3.0.1"

WORKDIR /plone/instance

COPY --chown=plone:plone buildout-base.cfg /plone/instance/buildout-base.cfg
COPY --chown=plone:plone buildout.cfg /plone/instance/buildout.cfg
COPY --chown=plone:plone src/ /plone/instance/src/

RUN mkdir -p var/filestorage var/blobstorage var/log var/.python-eggs && \
    chown -R plone:plone /plone/instance

USER plone

RUN buildout -c buildout.cfg

EXPOSE 8080
CMD ["bin/instance", "console"]