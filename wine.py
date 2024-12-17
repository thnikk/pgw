#!/usr/bin/python -u
import os
from subprocess import run


def init(prefix, wine) -> None:
    """ Initialize a wine prefix """
    env = os.environ.copy()
    env['WINEPREFIX'] = prefix
    run([wine, 'wineboot'], env=env, check=True)


def update() -> None:
    """ Update wine and tools """
    data_dir = os.path.expanduser('~/.local/share/pgw')
    temp_dir = os.path.join(data_dir, 'temp')
    runners_dir = os.path.join(data_dir, 'runners')
    # Download the latest version of wine to temp
    # Extract it to runners dir
    # Pull the latest dxvk
    # Extract it
    # Move files to prefix
    pass
