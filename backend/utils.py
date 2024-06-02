import json
import subprocess
import os


def sui_command(sui_commands, isJson=True, name="output"):
    if isJson:
        return json.loads(subprocess.check_output(["sui"] + sui_commands + ["--json"]))
    else:
        result = subprocess.run(["sui"] + sui_commands, capture_output=True, text=True)
        return {name: result.stdout.strip()}


def sui_command_with_pipe(sui_commands, isJson=False):
    print("sui_commands", ["sui"] + sui_commands + ["--json"])
    if isJson:
        process = subprocess.Popen(
            ["sui"] + sui_commands + ["--json"],
            stdout=subprocess.PIPE,
            text=True,
        )
    else:
        process = subprocess.Popen(
            ["sui"] + sui_commands,
            stdout=subprocess.PIPE,
            text=True,
        )
    output = []
    json_data = ""
    while True:
        line = process.stdout.readline()
        if not line:
            break
        if "{" in line or "[" in line or json_data != "":
            json_data += line.strip()
            isJson = True
        else:
            output.append(line.strip())
    if json_data != "":
        output.append(json.loads(json_data))
    print("output", output)
    return output


def sui_multi_command(sui_commands):
    process = subprocess.Popen(
        sui_commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    print(output, error)
    return None


def generic_command(command):
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    print(output, error)
    return output


def cat_command(file_path, isJson=True, name=None):
    expanded_path = os.path.expanduser(file_path)
    with open(expanded_path, "r") as f:
        file = json.load(f)
        if isJson:
            return json.loads(json.dumps(file))
        else:
            return {name: file}
