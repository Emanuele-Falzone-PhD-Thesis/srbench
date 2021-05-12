FROM python:3.8

RUN mkdir -p /data/input
RUN mkdir -p /data/output

WORKDIR /src

COPY group_by_timestamp.py .
COPY json-pg-serialize.py .

COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]