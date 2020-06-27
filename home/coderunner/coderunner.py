import subprocess

def compile_code(input_file):

    ret = {
        "compile_error" : False,
        "stderr" : None,
        "stdout" : None,
    }

    compile_result = subprocess.run(["g++", "-std=c++11" , input_file + ".cpp", "-o", input_file + ".exe"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if compile_result.returncode != 0:
        ret["compile_error"] = True
    
    ret["stderr"] = compile_result.stderr
    ret["stdout"] = compile_result.stdout

    return ret

def execute_code(input_file, input_string = None):

    ret = {
        "runtime_error" : False,
        "tle" : False,
        "stderr" : None,
        "stdout" : None,
    }
    
    try:
        execution_result = subprocess.run([input_file + ".exe"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input_string, timeout=2)
        
        if execution_result.returncode != 0:
            ret["runtime_error"] = True
        
        ret["stderr"] = execution_result.stderr
        ret["stdout"] = execution_result.stdout
    
    except:

        ret["tle"] = True
        

    return ret