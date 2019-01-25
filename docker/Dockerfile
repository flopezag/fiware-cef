# FIWARE-CEF
#
# VERSION 1.0.0

FROM python:3.7.2-alpine3.8
MAINTAINER Fernando López <fernando.lopez@fiware.org>

# Set the working directory to /opt/fiware-cef
WORKDIR /opt/fiware-cef

# Install software
RUN apk update && \
    apk upgrade && \
    apk add git && \
    rm -rf /var/cache/apk/* && \
    mkdir -p /opt/fiware-cef && \
    git clone https://github.com/flopezag/fiware-cef.git /opt/fiware-cef && \
    cd /opt/fiware-cef && \
    git checkout develop && \
    pip install --trusted-host pypi.python.org -r requirements.txt && \
    cp /opt/fiware-cef/jirasync/conf/jirasync.ini /etc/init.d/jirasync.ini && \
    for i in `find / -perm +6000 -type f`; do chmod a-s $i; done

USER 1000:1000

# Run jirasync.py when the container launches
CMD ["python", "./jirasync.py", "sync"]