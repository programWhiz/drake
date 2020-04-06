import os
import sys
import subprocess
from subprocess import PIPE


def run_cli_cmd(cmd):
    proc = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)
    print(proc.stdout.decode('utf-8'), file=sys.stdout)
    print(proc.stderr.decode('utf-8'), file=sys.stderr)
    return proc.returncode