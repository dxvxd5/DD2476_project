import os

from crawler.reader import Reader
from crawler.searcher import Searcher
from parser.Parser import Parser

def test():
    topic_path = os.path.join(os.path.dirname(__file__), "topics.json")
    config_path = os.path.join(os.path.dirname(__file__), "search_config.json")
    r = Reader(topic_path)
    r.parse()
    topic_list = r.topics

    #Parser
    p = Parser()
    p.hello("hahah")
    s = Searcher(topic_list, p.parse_file, config_path)
    s.search_and_upload()
    print("The End")

test()
