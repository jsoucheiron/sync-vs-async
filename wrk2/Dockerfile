FROM debian:latest

RUN apt-get update && apt-get install -y build-essential libssl-dev git zlib1g-dev
RUN git clone https://github.com/giltene/wrk2.git && \
    cd wrk2 && \
    make && \
    cp wrk /usr/local/bin

COPY test.sh /test.sh
