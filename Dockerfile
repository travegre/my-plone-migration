FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PLONE_VERSION 5.2.14

RUN apt-get update && apt-get install -y gcc build-essential libssl-dev libxml2-dev libxslt1-dev libz-dev libjpeg-dev libreadline-dev wv poppler-utils wget && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash plone

# Upgrade pip first, then install compatible buildout toolchain for Plone 5.2.14 on Python 3.8
RUN pip install --upgrade "pip==23.3.2" && \
    pip install --no-cache-dir "setuptools==67.6.0" "zc.buildout==3.0.1" "wheel"

WORKDIR /plone/instance

COPY --chown=plone:plone buildout-base.cfg /plone/instance/buildout-base.cfg
COPY --chown=plone:plone buildout.cfg /plone/instance/buildout.cfg
COPY --chown=plone:plone src/ /plone/instance/src/

RUN mkdir -p var/filestorage var/blobstorage var/log var/.python-eggs && chown -R plone:plone /plone/instance

USER plone

RUN buildout -c buildout.cfg

EXPOSE 8080
CMD ["bin/instance", "console"]