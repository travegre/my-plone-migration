FROM python:2.7-slim

ENV PYTHONUNBUFFERED 1
ENV PLONE_VERSION 4.3.20

# Debian Buster is EOL - redirect apt to the archive mirror
RUN sed -i \
    -e 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' \
    -e 's|http://security.debian.org/debian-security|http://archive.debian.org/debian-security|g' \
    -e '/buster-updates/d' \
    /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libz-dev \
    libjpeg-dev \
    libreadline-dev \
    wv \
    poppler-utils \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash plone

# setuptools 44.x and zc.buildout 2.13.x are the last versions
# supporting Python 2.7 and Plone 4.3
RUN pip install --no-cache-dir \
    zc.buildout==2.13.8 \
    setuptools==44.1.1

WORKDIR /plone/instance

# Copy only buildout configuration and package metadata needed to resolve
# dependencies before the expensive buildout layer.  Ordinary source/tool
# edits are copied later and therefore do not invalidate dependency installs.
COPY --chown=plone:plone buildout-base.cfg /plone/instance/buildout-base.cfg
COPY --chown=plone:plone buildout.cfg /plone/instance/buildout.cfg

# Develop eggs listed in buildout.cfg must exist when buildout runs.  Copy the
# package trees here; docker-compose bind-mounts ./src at runtime, so future
# script/source edits do not require an image rebuild at all.  This layer is
# only invalidated when the dependency-bearing src tree itself changes.
COPY --chown=plone:plone src/ /plone/instance/src/

RUN mkdir -p var/filestorage var/blobstorage var/log var/.python-eggs products && \
    chown -R plone:plone /plone/instance

USER plone

RUN buildout -c buildout.cfg

EXPOSE 8090
CMD ["bin/instance", "console"]
