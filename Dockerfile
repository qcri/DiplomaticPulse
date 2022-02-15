FROM python:3.8-slim
LABEL maintainer=Abdelkader

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN apt-get update \
    && apt-get install -y \
            libxml2-dev \
            libxslt-dev \
            gcc \
            wget \
            gnupg \
    && rm -rf /var/cache/apk/*

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip3 install -U --no-cache-dir pip

WORKDIR /code
COPY . /code
RUN python3 -m pip install -r requirements.txt && pip3 install --upgrade pymupdf && python3 -m pip install  scrapyd scrapyd-client

EXPOSE 6800

ENV PYTHONPATH=/code
CMD ./run_scrapyd.sh

