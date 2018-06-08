FROM python:3.6-alpine3.7

# Set directories
RUN mkdir -p /etc/micro/plugins
RUN mkdir -p /var/log/micro
RUN mkdir -p /var/run/micro

ENV MICRO_PLUGIN_PATH=/etc/micro/plugins
ENV MICRO_LOG_PATH=/var/log/micro
ENV MICRO_PID_PATH=/var/run/micro

RUN pip install micro

CMD python -m micro && tail -f /dev/null
