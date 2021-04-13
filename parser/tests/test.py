from parser.Parser import Parser
from elastic.Elastic_Search import ElasticSearch

p = Parser()
e = ElasticSearch()

output = p.parse_file(file='example_notebook.ipynb', repo_name='repo_name', repo_url='repo_url', repo_stars='repo_stars', is_kth='is_kth', kth_course_code='kth_course_code')

for i in output:
    e.save_object(object=i)




