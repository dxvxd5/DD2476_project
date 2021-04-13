import json

from elasticsearch_dsl import connections

connection = connections.create_connection(hosts=['localhost'], timeout=20)


class ElasticSearch:

    def save_object(self, object):
        connection.index(index="dd2476_project", body=json.dumps(object.__dict__))
