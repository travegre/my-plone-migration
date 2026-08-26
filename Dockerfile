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

# Dependency configuration gets its own cache boundary.
COPY --chown=plone:plone buildout-base.cfg /plone/instance/buildout-base.cfg
COPY --chown=plone:plone buildout.cfg /plone/instance/buildout.cfg

# Buildout needs the develop eggs to exist while it resolves/install packages,
# but migration scripts and export payloads do not belong in this expensive
# layer. Keep this explicit list in sync with [buildout] develop in buildout.cfg.
COPY --chown=plone:plone src/imiimenik.podoba/ /plone/instance/src/imiimenik.podoba/
COPY --chown=plone:plone src/imiimenik.produkti/ /plone/instance/src/imiimenik.produkti/
COPY --chown=plone:plone src/dezurstva.podoba/ /plone/instance/src/dezurstva.podoba/
COPY --chown=plone:plone src/dezurstva.produkti/ /plone/instance/src/dezurstva.produkti/
COPY --chown=plone:plone src/kiestra.podoba/ /plone/instance/src/kiestra.podoba/
COPY --chown=plone:plone src/kiestra.produkti/ /plone/instance/src/kiestra.produkti/
COPY --chown=plone:plone src/preiskave.podoba/ /plone/instance/src/preiskave.podoba/
COPY --chown=plone:plone src/preiskave.produkti/ /plone/instance/src/preiskave.produkti/
COPY --chown=plone:plone src/nadomescanja.podoba/ /plone/instance/src/nadomescanja.podoba/
COPY --chown=plone:plone src/nadomescanja.produkti/ /plone/instance/src/nadomescanja.produkti/
COPY --chown=plone:plone src/collective.easyform/ /plone/instance/src/collective.easyform/

RUN mkdir -p var/filestorage var/blobstorage var/log var/.python-eggs products && \
    chown -R plone:plone /plone/instance

USER plone

RUN buildout -c buildout.cfg

# At runtime docker-compose bind-mounts ./src over /plone/instance/src, so
# edits to package code and migration scripts are immediately visible without
# rebuilding the image. Only dependency/config changes require a rebuild.

EXPOSE 8090
CMD ["bin/instance", "console"]
