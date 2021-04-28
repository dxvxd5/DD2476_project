import ast
from elasticsearch_dsl import connections
import json
from comment_parser import comment_parser

connection = connections.create_connection(hosts=['localhost'], timeout=20)

class Parser:
    """
    This class is used to pars a python file, extract the methods
    and create the object we want to store in elastic search
    """

    # def parse_file(self, file, repo_name, repo_url, repo_stars, is_kth, kth_course_code):
    def parse_file(self, file):

        # Get the file content
        text = file.file_content

        try:
            # Convert if notbook
            if file.file_ext == '.ipynb':
                text = self.notebook_to_py(text)

            # Flag to save the full script if no funtion
            raw_script = True

            # Split the line to extract the code block later
            lines = text.splitlines()


            # Extract and loop through the nodes in the file
            p = ast.parse(text)
            for node in ast.walk(p):
                if isinstance(node, ast.FunctionDef):
                    # Function found -> not saving as a raw script
                    raw_script = False

                    # Extract code block
                    start = node.lineno
                    end = node.end_lineno
                    code_block = '\n'.join(lines[start - 1:end])

                    # Parse the comment and the variable name
                    metastrings = self.get_metastrings(code_block)

                    # Create object to save in elasticsearch
                    functionObject = FunctionObject(node.name, code_block, file.repo_name, file.repo_url, file.stars, file.from_kth,
                                                    file.course, metastrings)

                    # Save the object to elasticsearch
                    connection.index(index="dd2476_project", body=json.dumps(functionObject.__dict__))

            # If no function has been found in the file
            if raw_script:

                # Parse the comment and the variable name
                metastrings = self.get_metastrings(text)

                # Create object to save in elasticsearch
                raw_object = FunctionObject('Raw - ' + file.repo_name, text, file.repo_name, file.file_url, file.stars, file.from_kth,
                                            file.course, metastrings)

                # Save the object to elasticsearch
                connection.index(index="dd2476_project", body=json.dumps(raw_object.__dict__))

        except:
            # Ignore the file if ast can't parse it
            pass

    def notebook_to_py(self, notebook):
        j = json.loads(notebook)
        output = ''
        if j["nbformat"] >= 4:
            for i, cell in enumerate(j["cells"]):
                #output += ("#cell " + str(i) + "\n")
                for line in cell["source"]:
                    if cell["cell_type"] == 'code':
                        output += line
                output += '\n\n'
        else:
            for i, cell in enumerate(j["worksheets"][0]["cells"]):
                #output += ("#cell " + str(i) + "\n")
                if cell["cell_type"] == 'code':
                    for line in cell["input"]:
                        output += line
                output += '\n\n'

        return output

    def get_metastrings(self, code_block):

        # Extract comment list
        comments_list = comment_parser.extract_comments_from_str(code_block, mime='text/x-python')
        comments = [comment.text() for comment in comments_list]

        # Extract variables names -> better way is welcome
        variable_name = [line.split('=')[0].strip() for line in code_block.split('\n') if len(line.split('=')[0].strip())<20 and ('=' in line)and not line.strip().startswith(('def', 'return'))]
        metastrings = ' '.join((comments + variable_name))

        return metastrings


class FunctionObject(object):
    def __init__(self, function_name, function_code, repo_name, repo_url, repo_stars, isKth, kth_course_code, metastrings):
        self.function_name = function_name
        self.function_code = function_code
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.repo_stars = repo_stars
        self.isKth = isKth
        self.kth_course_code = kth_course_code
        self.metastrings = metastrings
