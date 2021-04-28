import json
import os

from github import Github


class Searcher:
    """
    This class represents the searcher that will
    search for repos related to the given topics
    """

    class File:
        """
        Helper class that represents a file
        in a repository
        """

        def __init__(
            self,
            stars,
            from_kth,
            course,
            repo_name,
            repo_url,
            repo_forks,
            file_name,
            file_url,
            file_content,
            file_ext
        ):
            self.stars = stars
            self.from_kth = from_kth
            self.course = course
            self.repo_name = repo_name
            self.repo_url = repo_url
            self.repo_forks = repo_forks
            self.file_name = file_name
            self.file_url = file_url
            self.file_content = file_content
            self.file_ext = file_ext

        def __str__(self):
            return "File %s \n from repo %s, stars: %d, forks: %d, from_kth: %s, course: %s" % (
                self.file_name,
                self.repo_name,
                self.stars,
                self.repo_forks,
                self.from_kth,
                self.course
            )

    def __init__(
        self,
        topics,
        uploader,
        config_path,
    ):

        if len(topics) == 0:
            raise ValueError("The list of topics is empty")

        # reading the config json file
        with open(config_path, "r") as f:
            config = json.load(f)

            self.languages = config["languages"]
            # file extensions to look for
            self.extensions = config["extensions"]
            # file names (without extension) to avoid (ex: __init__)
            self.avoid_files = config["avoid_files"]
            # repo names to avoid (ex: repos of big libraries like 
            # "keras" or "tensorflow")
            self.avoid_repos = config["avoid_repos"]
            # github api object
            self.github = Github(login_or_token=config["github_access_token"])
            # number max of repos to search for each topic
            self.repo_per_query = config["repo_per_query"]

            f.close()

        self.topics = topics
        self.nr_topics = len(topics)

        # the index of the current topic to search
        self.current_topic = -1

        # set to true when all the topics have been searched
        self.no_more_topics = False

        # function to be used to upload the files to
        # elasticsearch
        self.uploader = uploader

        # A dictionary with all the repos searched
        # so far. Need this to avoid duplicates
        self.checked_repos = dict()

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

        # It is impossible to query many languages at once
        # So create one query for each language
        queries = [
            "%s in:name,readme,description language:%s" % (keyword, language)
            for language in self.languages
        ]

        return queries

    def search_and_upload(self):
        """
        Search for the topics in Github and upload the results
        """

        topic = self.get_next_topic()
        while topic is not None:
            # To each topic is associated a list of keywords.
            # We search for all those keywords
            # the topic name is also a keyword to search
            keywords = [topic.topic] + topic.keywords

            for keyword in keywords:
                # get the queries for each language
                queries = self.build_query(keyword)

                # If the current keyword is the topic name,
                # and the topic is a KTH course, we assume that
                # the resulting repositories will be from KTH
                if topic.is_kth_course and keyword == topic.topic:
                    from_kth = True
                else:
                    from_kth = False

                for query in queries:
                    # the total number of uploaded repos for this query
                    repo_count = 0
                    # the index of the repo in the result list
                    repo_index = 0

                    # Get the repos corresponding to the query
                    repositories = self.github.search_repositories(query)

                    while repo_count < self.repo_per_query and repo_index < repositories.totalCount:
                        repository = repositories[repo_index]

                        if repository.id in self.checked_repos or repository.name in self.avoid_repos:
                            repo_index += 1
                            continue

                        if from_kth:
                            course_name = topic.topic
                        else:
                            course_name = None

                        self.upload_repo_files(repository, from_kth, course_name)

                        self.checked_repos.update({repository.id: True})
                        repo_index += 1
                        repo_count += 1

            topic = self.get_next_topic()

    def upload_repo_files(self, repo, from_kth, course_name):
        """
        Upload all files in the repository with the uploader
        The uploaded files match the config spec
        """

        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)

            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file_base_name, file_ext = os.path.splitext(file_content.name)

                # make sure we upload the non-blacklisted files
                # having the right extension
                if file_ext in self.extensions and not file_base_name in self.avoid_files:

                    #? The Github API file up to 1MB in size
                    # 1024*1024 = 1048576
                    if (file_content.size < 1048576):
                        try:
                            file = Searcher.File(
                                repo.stargazers_count,
                                from_kth,
                                course_name,
                                repo.name,
                                repo.html_url,
                                repo.forks_count,
                                file_content.name,
                                file_content.html_url,
                                file_content.decoded_content.decode(),
                                file_ext
                            )
                            self.uploader(file)
                        except AssertionError:
                            continue
