FROM docker.elastic.co/logstash/logstash:8.19.18
RUN logstash-plugin install logstash-output-loki
RUN logstash-plugin install logstash-output-syslog