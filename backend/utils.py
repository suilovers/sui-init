import json
import subprocess
import os


def sui_command(sui_commands, isJson=True, name=None):
    if isJson:
        return json.loads(subprocess.check_output(["sui"] + sui_commands + ["--json"]))
    else:
        result = subprocess.run(["sui"] + sui_commands, capture_output=True, text=True)
        return {name: result.stdout.strip()}

def sui_multi_command(sui_commands):
    process = subprocess.Popen(sui_commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    print(output, error)
    return None

def cat_command(file_path, isJson=True, name=None):
    expanded_path = os.path.expanduser(file_path)
    with open(expanded_path, "r") as f:
        file = json.load(f)
        if isJson:
            return json.loads(json.dumps(file))
        else:
            return {name: file}
