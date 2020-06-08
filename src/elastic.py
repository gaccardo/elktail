import configparser
from elasticsearch import Elasticsearch
from datetime import datetime

import configuration


def connect():
    config = configuration.get_config()
    return Elasticsearch(
        [config['host']],
        http_auth=(config['username'], config['password']),
        scheme=config['scheme'], port=config['port']
    )


def get_search_body(iso_date, project=None, process_type=None):
    body = {
        "source": {
            "size": 10000,
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": f"{iso_date}Z"
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
    if project is not None:
        body['source']['query']['bool']['must'].append(
            {
                'match': {
                    'fields.project.keyword': project
                }
            }
        )
    if process_type is not None:
        body['source']['query']['bool']['must'].append(
            {
                'match': {
                    'fields.process_type.keyword': process_type
                }
            }
        )
    return body


def search(es, body):
    now = datetime.now()
    return es.search_template(
        body,
        index=f"filebeat-{now.year}.{now.month:02}.{now.day:02}"
    )

