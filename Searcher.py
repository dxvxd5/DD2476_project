from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Document, Text, Boolean, Integer
from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'])
class MyDoc(Document):
    function_name = Text()
    function_code = Text()
    repo_name = Text()
    repo_url = Text()
    repo_stars = Integer()
    isKth = Boolean()
    kth_course_code = Text()

    class Index:
        name = 'dd2476_project'

class Searcher:


    def __init__(self):
        self.client = Elasticsearch()

    def search(self, query, course_code=None):
        
        q = query + " " + course_code if course_code != None else query
        s = Search(using=self.client, index='dd2476_project').query("multi_match", query=q, fields=['function_name', 'kth_course_code'])
        response = s.execute()
      
        return response.to_dict()['hits']['hits']


    def test(self):
        s = Search(using=self.client,index='dd2476_project')
        results = s.execute()
        print(s.count())
        print(results.hits.total)
        for hit in s:
            print(hit.to_dict())
       

if __name__=="__main__":
    s = Searcher()

    s.search("quicksort","DD2476")
