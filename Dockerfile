FROM python:3.8-alpine

COPY requirements.txt /requirements.txt
RUN apk update && apk add chromium chromium-chromedriver tzdata && pip install -r requirements.txt && cp /usr/share/zoneinfo/America/New_York /etc/localtime && echo "America/New_York" > /etc/timezone

COPY checker.py /checker.py
COPY crontab.txt /etc/crontabs/root

CMD ["crond", "-f", "-d", "8"]