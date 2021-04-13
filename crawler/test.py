import os

from crawler.reader import Reader
from crawler.searcher import Searcher


def test():
    path = os.path.join(os.path.dirname(__file__), "topics.json")
    r = Reader(path)
    r.parse()
    s = Searcher(r.topics)
    res = s.search_next_topic()
    print("The End")


test()
