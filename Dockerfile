FROM alpine:latest

RUN mkdir -p /app ; \
    apk add --update --no-cache python3; \
    python3 -m ensurepip; \
    pip3 install --no-cache --upgrade \
      pip setuptools requests mysql-connector-python; \
    ln -s /usr/bin/python3 /usr/bin/python

COPY . /app

CMD [ "/app/run.py" ]

