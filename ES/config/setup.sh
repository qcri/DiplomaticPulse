#!/bin/sh

echo Initiating Elasticsearch Custom Index
# move to the directory of this setup script
cd "$(dirname "$0")"

until $(curl -sSf -XGET --insecure --user elastic:changeme 'http://localhost:9200/_cluster/health?wait_for_status=yellow' > /dev/null); do
    printf 'AUTHENTICATION ERROR DUE TO X-PACK, trying again in 5 seconds \n'
    sleep 5
done

#delete index
curl -XDELETE localhost:9200/countries
curl -XDELETE localhost:9200/urlconfig

# create  index:
curl -X PUT "localhost:9200/countries?pretty"
curl -X PUT "localhost:9200/urlconfig?pretty"
curl -X PUT "localhost:9200/dppa.st?pretty"

# upload data from json file
curl -X PUT "localhost:9200/urlconfig/_bulk?pretty" -H 'Content-Type: application/x-ndjson' --data-binary @./init_indices/urlconfig.json
curl -X PUT "localhost:9200/countries/_bulk?pretty" -H 'Content-Type: application/x-ndjson' --data-binary @./init_indices/countries.json
curl -X PUT "localhost:9200/dppa.st/_bulk?pretty" -H 'Content-Type: application/x-ndjson' --data-binary @./init_indices/dppa.st.json