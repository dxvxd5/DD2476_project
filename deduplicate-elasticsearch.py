#!/usr/local/bin/python3

# A description and analysis of this code can be found at 
# https://alexmarquardt.com/2018/07/23/deduplicating-documents-in-elasticsearch/

import hashlib
from elasticsearch import Elasticsearch, helpers
from functools import reduce
ES_HOST = 'localhost:9200'
ES_USER = 'elastic'
ES_PASSWORD = 'elastic'

es = Elasticsearch([ES_HOST], http_auth=(ES_USER, ES_PASSWORD))
dict_of_duplicate_docs = {}

# The following line defines the fields that will be
# used to determine if a document is a duplicate
keys_to_include_in_hash = ["function_name", "function_code", "repo_name", "repo_url", "repo_stars", "isKth", "kth_course_code", "metastrings"]


# Process documents returned by the current search/scroll
def populate_dict_of_duplicate_docs(hit):

    combined_key = ""
    for mykey in keys_to_include_in_hash:
        combined_key += str(hit['_source'][mykey])

    _id = hit["_id"]

    hashval = hashlib.md5(combined_key.encode('utf-8')).digest()

    # If the hashval is new, then we will create a new key
    # in the dict_of_duplicate_docs, which will be
    # assigned a value of an empty array.
    # We then immediately push the _id onto the array.
    # If hashval already exists, then
    # we will just push the new _id onto the existing array
    dict_of_duplicate_docs.setdefault(hashval, []).append(_id)


# Loop over all documents in the index, and populate the
# dict_of_duplicate_docs data structure.
def scroll_over_all_docs():
    for hit in helpers.scan(es, index='dd2476_project'):
        populate_dict_of_duplicate_docs(hit)


def loop_over_hashes_and_remove_duplicates():
    # Search through the hash of doc values to see if any
    # duplicate hashes have been found
    for hashval, array_of_ids in dict_of_duplicate_docs.items():
      if len(array_of_ids) > 1:
        print("********** Duplicate docs hash=%s **********" % hashval)
        # Get the documents that have mapped to the current hasval
        #matching_docs = es.mget(index="dd2476_project", doc_type="doc", body={"ids": array_of_ids})
        q = {
                "query": {
                    "terms": {
                        "_id": array_of_ids 
                    }
                }
            }
        matching_docs = es.search(index='dd2476_project', body=q)['hits']['hits']
        temp = []
        ids_to_delete = []
        og = matching_docs[0]["_source"]
        for i, doc in enumerate(matching_docs[1:]):
            # In order to remove the possibility of hash collisions,
            # write code here to check all fields in the docs to
            # see if they are truly identical - if so, then execute a
            # DELETE operation on all except one.
            # In this example, we just print the docs.
            #print("doc=%s\n" % doc['_source'])
            #temp.append(doc["_source"])
            d = doc["_source"]
            for key in keys_to_include_in_hash:
                temp.append(og[key] == d[key])
            #f_n = og["function_name"] == d["function_name"]
            #print(og["function_name"] == d["function_name"])
            all_equal = len(set(temp)) == 1 and set(temp) == {True}
            if(all_equal):
                ids_to_delete.append(array_of_ids[i+1])
        query = {"query": {"terms": {"_id": ids_to_delete}}}
        res = es.delete_by_query(index='dd2476_project', body=query)
        #print(res)
        #print(og)
        #print(temp)


def main():
    scroll_over_all_docs()
    loop_over_hashes_and_remove_duplicates()


main()