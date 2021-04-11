import json
import os


class Reader:
    """
    This class represents a JSON reader that will
    create a list of Topic objects corresponding to
    the JSON document
    """

    class Topic:
        """
        Helper class that represents a topic to search for in Github
        Typically, it consists of a topic and a list of
        related keywords
        """

        def __init__(self, topic, keywords, course):
            if not ((type(topic), type(keywords), type(course)) == (str, list, bool)):
                raise TypeError("Type error in the JSON file. Check it!")

            self.topic = topic
            self.keywords = [topic] + keywords
            self.isCourse = course

    def __init__(self, path):
        self.json_path = path
        # the content of the JSON file in a dictionary format
        self.json_dic = None
        # list of all the topics in the JSON file
        self.topics = []

    def read(self):
        f = open(self.json_path, "r")
        self.json_dic = json.load(f)
        f.close()

    def insert_topic(self, topic, value):
        t = Reader.Topic(topic, value["keywords"], value["course"])
        self.topics.append(t)

    def parse(self):
        """
        Go through the element of the JSON dictionary
        and insert the topics into the list of topics
        """

        if not self.json_dic:
            self.read()

        for topic, value in self.json_dic.items():
            self.insert_topic(topic, value)
