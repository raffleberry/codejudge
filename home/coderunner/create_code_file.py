import os
from .random_string import random_string

def create_code_file(code):
    filename = random_string(8)
    code_tmp_dir = os.path.join(os.path.dirname(__file__), "tmp")
    code_file = os.path.join(code_tmp_dir, filename)
    with open(code_file + ".cpp" , "w") as fl:
        fl.write(code)
    return code_file