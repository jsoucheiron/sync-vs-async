FROM alpine:latest

ENV VEGETA_VERSION 6.3.0

ADD https://github.com/tsenart/vegeta/releases/download/v${VEGETA_VERSION}/vegeta-v${VEGETA_VERSION}-linux-amd64.tar.gz /tmp/vegeta.tar.gz
RUN cd /bin && tar -zxvf /tmp/vegeta.tar.gz && chmod +x /bin/vegeta && rm /tmp/vegeta.tar.gz

COPY test.sh /test.sh
