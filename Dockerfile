FROM python:3.6-alpine3.6

# Define config location
ENV NOTIFIER_CONFIG=/etc/notifier/config/config.json

# Set directories
RUN mkdir -p /etc/notifier/config
RUN mkdir /etc/notifier/plugins
RUN mkdir /var/log/notifier
RUN mkdir /var/run/notifier

# install application
RUN mkdir /notifier
COPY . /notifier
RUN pip install /notifier
RUN rm -rf /notifier

CMD python -m notifier && tail -f /dev/null
