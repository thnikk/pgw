#!/usr/bin/python -u
from subprocess import Popen, PIPE
import sys


def fzf(input_list, prompt=None) -> str:
    """ Get selection from list """
    command = ["fzf", "-m", "--tac"]
    if prompt:
        command.append(f'--prompt={prompt}')
    with Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE) as fzf:
        selection = fzf.communicate(
            input=bytes("\n".join(input_list), 'utf-8'))[0]
        if fzf.returncode != 0:
            sys.exit(1)
        return selection.decode().strip()


def fuzzel(input_list, prompt="") -> str:
    """ Get selection from list with custom prompt """
    length = str(min(len(input_list), 8))
    with Popen(
        ["fuzzel", "--dmenu", "-l", length, "-p", prompt],
        stdin=PIPE, stdout=PIPE, stderr=PIPE
    ) as fuzzel:
        selection = fuzzel.communicate(
            input=bytes("\n".join(input_list), 'utf-8'))[0]
        if fuzzel.returncode != 0:
            sys.exit(1)
        return selection.decode().strip()
