FROM docker.elastic.co/elasticsearch/elasticsearch:7.10.1
#RUN bin/elasticsearch-plugin install analysis-icu

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN mkdir utils
COPY utils/wait-for-it.sh utils/wait-for-it.sh

USER root
RUN chmod +x /docker-entrypoint.sh utils/wait-for-it.sh
RUN chown -R elasticsearch:elasticsearch /docker-entrypoint.sh utils/wait-for-it.sh

USER elasticsearch
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["elasticsearch"]
