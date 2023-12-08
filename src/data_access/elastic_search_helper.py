from elasticsearch import Elasticsearch

es = Elasticsearch(
    [
        {"host": "host1-ip-address", "port": port-number}, 
        {"host": "host2-ip-address", "port": port-number},
        {"host": "host3-ip-address", "port": port-number}
    ],
    http_auth=("username", "secret"), 
    timeout=3600
)