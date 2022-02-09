FROM python:3.8-slim
LABEL maintainer=Abdelkader

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN apt-get update \
    && apt-get install -y \
            libxml2-dev \
            libxslt-dev \
            gcc \
    && rm -rf /var/cache/apk/*

RUN pip3 install -U --no-cache-dir pip

WORKDIR /code
COPY . /code
RUN python3 -m pip install -r requirements.txt && pip3 install --upgrade pymupdf && python3 -m pip install  scrapyd scrapyd-client

EXPOSE 6800

ENV PYTHONPATH=/code
CMD ./run_scrapyd.sh

