import os
from .coderunner import compile_code, execute_code
from .create_code_file import create_code_file

def join(left, right):
    return os.path.join(left, right)

def question(code, question, pts_dist):

    ret = {
        "invalid" : None,
        "data" : None,
        "points": 0
    }

    current_dir = os.path.dirname(__file__)
    data_dir = join(current_dir, "data")
    q_dir_path = join(data_dir, question)
    if os.path.exists(q_dir_path):
        tests = list(pts_dist.keys())

        exec_result = []
        
        code_file = create_code_file(code)

        compile_result = compile_code(code_file)

        if compile_result["compile_error"] == False:

            for test in tests:
                input_file = open(join(q_dir_path, test + ".in"))
                output_file = open(join(q_dir_path, test + ".out"))
                
                input_data = ''.join(input_file.readlines())
                output_data = ''.join(output_file.readlines())
                
                input_file.close()
                output_file.close()

                result = execute_code(code_file, input_data)
                exec_output = result["stdout"]
                result["points"] = pts_dist[test]
                
                if result["runtime_error"] == False and result["tle"] == False and exec_output.rstrip() == output_data.rstrip():
                    result["verdict"] = "Accepted"
                    ret["points"] += pts_dist[test]
                else:
                    result["verdict"] = "Wrong Answer"

                result.pop("stdout")
                
                result.pop("stderr")
                
                exec_result.append(result)

            ret["data"] = exec_result

        else:

            ret["invalid"] = "Code"
            ret["data"] = compile_result
        
        if (os.path.exists(code_file + ".cpp")):
            os.remove(code_file + ".cpp")
        # if (os.path.exists(code_file + ".exe")):
        #     os.remove(code_file + ".exe")

    else:
        ret["invalid"] = "question"
        ret["data"] = "question data doesn't exist"

    return ret
