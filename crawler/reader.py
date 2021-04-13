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

        def __init__(self, topic, keywords, is_kth_course):
            if not (
                (type(topic), type(keywords), type(is_kth_course)) == (str, list, bool)
            ):
                raise TypeError("Type error in the JSON file. Check it!")

            self.topic = topic
            # the keywords related to this topic
            self.keywords = keywords
            # if this topic is a KTH course
            self.is_kth_course = is_kth_course

        def __str__(self):
            return "Topic %s: Keywords %s" % (self.topic, self.keywords)

    def __init__(self, path):
        self.topic_path = path
        # the content of the JSON file in a dictionary format
        self.topic_dic = None
        # list of all the topics in the JSON file
        self.topics = []

    def read(self):
        f = open(self.topic_path, "r")
        self.topic_dic = json.load(f)
        f.close()

    def insert_topic(self, topic, value):
        t = Reader.Topic(topic, value["keywords"], value["isKTHCourse"])
        self.topics.append(t)

    def parse(self):
        """
        Go through the element of the JSON dictionary
        and insert the topics into the list of topics
        """

        if not self.topic_dic:
            self.read()

        for topic, value in self.topic_dic.items():
            self.insert_topic(topic, value)
