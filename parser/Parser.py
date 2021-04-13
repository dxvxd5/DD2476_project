import ast
from elasticsearch_dsl import connections
import json


class Parser:

    """
    This class is used to pars a python file, extract the methods
    and create the object we want to store in elastic search
    """

    def parse_file(self, file, repo_name, repo_url, repo_stars, is_kth, kth_course_code):

        fileObject = open(file, "r")
        text = fileObject.read()

        if file.endswith('.ipynb'):
            text = self.notebook_to_py(text)

        if file.endswith('.py') or file.endswith('ipynb'):

            lines = text.splitlines()
            p = ast.parse(text)
            for node in ast.walk(p):
                if isinstance(node, ast.FunctionDef):
                        start = node.lineno
                        end = node.end_lineno
                        code_block = '\n'.join(lines[start-1:end])
                        functionObject = FunctionObject(node.name, code_block, repo_name, repo_url, repo_stars, is_kth, kth_course_code)
                        yield functionObject
        else:
            print(file.split(".")[-1], 'files extension are not supported by the parser')


    def notebook_to_py (self, notebook):
        j = json.loads(notebook)
        output = '' # output.py
        if j["nbformat"] >= 4:
            for i, cell in enumerate(j["cells"]):
                output+=("#cell " + str(i) + "\n")
                for line in cell["source"]:
                    if cell["cell_type"] == 'code':
                        output+=line
                output+='\n\n'
        else:
            for i, cell in enumerate(j["worksheets"][0]["cells"]):
                output+=("#cell " + str(i) + "\n")
                for line in cell["input"]:
                    if cell["cell_type"] == 'code':
                        output += line
                output+='\n\n'

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