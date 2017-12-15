FROM python:3.6-alpine3.6

# Define config location
ENV MICRO_CONFIG=/etc/micro/config/config.json

# Set directories
RUN mkdir -p /etc/micro/config
RUN mkdir /etc/micro/plugins
RUN mkdir /var/log/micro
RUN mkdir /var/run/micro

# install application
RUN mkdir /micro
COPY . /micro
RUN pip install /micro
RUN rm -rf /micro

CMD python -m micro && tail -f /dev/null
