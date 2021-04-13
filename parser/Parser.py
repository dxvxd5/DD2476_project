import ast
from elasticsearch_dsl import connections
import json


class Parser:
    """
    This class is used to pars a python file, extract the methods
    and create the object we want to store in elastic search
    """

    # def parse_file(self, file, repo_name, repo_url, repo_stars, is_kth, kth_course_code):
    def parse_file(self, file):

        print("parser in")
        text = file.file_content

        if file.file_ext == '.ipynb':
            text = self.notebook_to_py(text)

        raw_script = True

        lines = text.splitlines()
        p = ast.parse(text)
        for node in ast.walk(p):
            if isinstance(node, ast.FunctionDef):
                raw_script = False
                start = node.lineno
                end = node.end_lineno
                code_block = '\n'.join(lines[start - 1:end])
                functionObject = FunctionObject(node.name, code_block, file.repo_name, file.repo_url, file.stars, file.from_kth,
                                                file.course)
                yield functionObject

        if raw_script:
            raw_object = FunctionObject('Raw - ' + file, text, file.repo_name, file.file_url, file.stars, file.from_kth,
                                        file.course)
            yield raw_object

    def hello(self, string):
        print(string)

    def notebook_to_py(self, notebook):
        j = json.loads(notebook)
        output = ''
        if j["nbformat"] >= 4:
            for i, cell in enumerate(j["cells"]):
                output += ("#cell " + str(i) + "\n")
                for line in cell["source"]:
                    if cell["cell_type"] == 'code':
                        output += line
                output += '\n\n'
        else:
            for i, cell in enumerate(j["worksheets"][0]["cells"]):
                output += ("#cell " + str(i) + "\n")
                for line in cell["input"]:
                    if cell["cell_type"] == 'code':
                        output += line
                output += '\n\n'

        return output


class FunctionObject(object):
    def __init__(self, function_name, function_code, repo_name, repo_url, repo_stars, isKth, kth_course_code):
        self.function_name = function_name
        self.function_code = function_code
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.repo_stars = repo_stars
        self.isKth = isKth
        self.kth_course_code = kth_course_code
