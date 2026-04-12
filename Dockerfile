FROM plone/plone:4.3

USER root

RUN echo "deb http://archive.debian.org/debian stretch main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list && \
    echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until

RUN apt-get update && apt-get install -y gcc build-essential python-dev \
    && rm -rf /var/lib/apt/lists/*

RUN rm -rf /plone/instance/var/filestorage \
           /plone/instance/var/blobstorage

COPY --chown=plone:plone src/ /plone/instance/src/
COPY --chown=plone:plone buildout.cfg /plone/instance/buildout.cfg

USER plone
WORKDIR /plone/instance
RUN /usr/local/bin/buildout -c buildout.cfg

EXPOSE 8080
CMD ["bin/instance", "console"]
