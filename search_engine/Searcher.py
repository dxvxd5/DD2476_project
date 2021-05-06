from elasticsearch import Elasticsearch

class Searcher:
    def __init__(self):
        self.client = Elasticsearch()

    def search(self, query, course_code=None):
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
                            "function_name^2",
                            "metastrings"
                        ],
                        "minimum_should_match": "80%",
                        "type":"most_fields"
                    }
                }
            )
        if course_code:
            temp["query"]["bool"]["should"].append(
                {
                    "match": {
                        "kth_course_code": {
                            "query": course_code,
                            "minimum_should_match": "100%",
                            "boost": "10"
                        }
                    }
                }
            )
        test = self.client.search(index='dd2476_project', body=temp)
        return test['hits']['hits']
        
