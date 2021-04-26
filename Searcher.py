from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])

class Searcher:


    def __init__(self):
        self.client = Elasticsearch()

    def search(self, query, course_code=None):
        
        #q = query + " " + course_code if course_code != None else query
        #s = Search(using=self.client, index='dd2476_project').query("regexp", query=q)#, fields=['function_name'])#, 'kth_course_code'])
        #response = s.execute()
        temp = {
            "size":100,
            "query": {
                    "bool": {
                        "should": [

                        ]
                    }
        }}
        if query:
            temp["query"]["bool"]["should"].append(
                {
                    "multi_match": {
                        "query": query,
                        "fields": [
                            "function_code",
                            "function_name"
                        ],
                        "minimum_should_match": "80%"
                    }
                }
            )
        if course_code:
            temp["query"]["bool"]["should"].append(
                {
                    "match": {
                        "kth_course_code": {
                            "query": course_code,
                            "minimum_should_match": "20%"
                        }
                    }
                }
            )
        test = self.client.search(index='dd2476_project', body=temp)
        return test['hits']['hits']
        
       
if __name__=="__main__":
    s = Searcher()

    s.search("quicksort","DD2476")
