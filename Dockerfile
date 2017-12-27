FROM python:3.6-alpine3.6

# Set directories
RUN mkdir -p /etc/micro/plugins
RUN mkdir -p /var/log/micro
RUN mkdir -p /var/run/micro

ENV MICRO_PLUGIN_PATH=/etc/micro/plugins
ENV MICRO_LOG_PATH=/var/log/micro
ENV MICRO_PID_PATH=/var/run/micro

# Install application
# This instructions copy and install the current
# code, this is doing in this way to allow test new
# implementations easy
RUN mkdir /micro
COPY . /micro
RUN pip install /micro
RUN rm -rf /micro

CMD python -m micro && tail -f /dev/null
