from github import Github


class Searcher:
    """
    This class represents the searcher that will
    search for repos related to the given topics
    """

    def __init__(self, topics):

        if len(topics) == 0:
            raise ValueError("The list of topics is empty")

        self.topics = topics
        self.nr_topics = len(topics)
        # github api object
        self.github = Github()
        # the index of the current topic to search
        self.current_topic = -1
        self.query = None
        # set to true when all the topics have been searched
        self.no_more_topics = False

    def get_next_topic(self):
        """
        return the next topic to search for if there is any
        """

        if self.no_more_topics:
            return None

        i = self.current_topic + 1
        if i >= self.nr_topics:
            self.no_more_topics = True
            return None
        else:
            self.current_topic = i
            return self.topics[self.current_topic]

    def build_query(self, keyword):
        """
        Build the query for the next topic to search for
        """

        # Is impossible to query to languages at once
        # So create one query for python and another for jupyter notebook
        py_query = "%s in:name,readme,description language:python" % keyword
        nb_query = "%s in:name,readme,description language:jupyter notebook" % keyword

        return py_query, nb_query

    def search_next_topic(self):
        topic = self.get_next_topic()

        # If there is no more topics, return None. To avoid this, check if there is a topic
        # (with no_more_token attribute) before seaching
        if topic is None:
            return None

        # To each is associated a list of keywords. We search for all those keywords
        k1 = topic.keywords[0]
        py_query, _ = self.build_query(k1)

        return self.github.search_repositories(py_query)