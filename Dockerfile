FROM python:3.10-bookworm
WORKDIR /code

# install python modules
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# install and set up server cronjobs
RUN apt-get update && \
    apt-get -y install cron
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab
RUN touch /var/log/cron.log


COPY . /code/

RUN chmod +rw /code
RUN chmod +x /code/containerstart.sh

EXPOSE 8000

CMD ["/bin/bash", "containerstart.sh"]

