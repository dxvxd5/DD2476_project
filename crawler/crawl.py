import os

from crawler.reader import Reader
from crawler.searcher import Searcher
from parser.Parser import Parser

def crawl_topic():
    # Will crawl the current topic in the file current_topic_to_search
    topic_path = os.path.join(os.path.dirname(__file__), ".settings", "current_topic_to_search.json")
    config_path = os.path.join(os.path.dirname(__file__), ".settings", "search_config.json")
    r = Reader(topic_path)
    r.parse()
    topic_list = r.topics

    #Parser
    p = Parser()
    s = Searcher(topic_list, p.parse_file, config_path)
    s.search_and_upload()
    print("The End")

crawl_topic()
