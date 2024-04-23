import json
import subprocess


def sui_command(sui_commands, isJson=True, name=None):
    if isJson:
        return json.loads(subprocess.check_output(['sui'] + sui_commands + ['--json']))
    else:
        result = subprocess.run(['sui'] + sui_commands, capture_output=True, text=True)
        return {name: result.stdout.strip()}