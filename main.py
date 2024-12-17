#!/usr/bin/python3 -u
from subprocess import Popen
import argparse
import json
import os
import re
import launchers


def parse_args() -> argparse.ArgumentParser:
    """ Parse arguments """
    parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     '-f', action='store_true', help='Use fuzzel instead of fzf')
    parser.add_argument('command', help='command to run')
    parser.add_argument('arguments', nargs='*', help='argument(s) for command')
    return parser.parse_args()


def get_config() -> dict:
    """ Ignore comments and get parsed json config"""
    with open(os.path.expanduser('~/.config/pgw.json'), 'r') as file:
        output = file.read()
        output = re.sub(re.compile(r"/\*.*?\*/", re.DOTALL), "", output)
        output = re.sub(re.compile(r"//.*?\n"), "", output)
        return json.loads(output)


def get_value(config, game_config, key) -> bool:
    try:
        return game_config[key] \
            if key in game_config else config[key]
    except KeyError:
        return False


def cache(selection) -> dict:
    """ Add the last opened game to the cache file """
    cache_file = os.path.expanduser('~/.cache/pgw.cache')
    try:
        with open(cache_file, 'r') as file:
            cache = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        cache = []
    cache = ([selection] + cache)[:20]
    with open(cache_file, 'w') as file:
        file.write(json.dumps(cache, indent=4))
    return cache


def sort_frequent(full_list) -> list:
    """ Get list of opened games from cache file
    and put most frequently opened at the top """
    cache_file = os.path.expanduser('~/.cache/pgw.cache')
    try:
        with open(cache_file, 'r') as file:
            opened_list = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        opened_list = []
    unique = set(opened_list)
    counted = {item: opened_list.count(item) for item in unique}
    frequent = list(dict(sorted(
        counted.items(), key=lambda x: x[1], reverse=True)))
    for item in frequent:
        try:
            full_list.remove(item)
        except ValueError:
            frequent.remove(item)
    return frequent + full_list


def main() -> None:
    env = os.environ.copy()
    args = parse_args()
    config = get_config()

    # Get list of games in config
    game_list = sorted(config["games"])
    frequent = sort_frequent(game_list)

    # Get game selection
    if args.command == 'fuzzel':
        selection = launchers.fuzzel(frequent)
    if args.command == 'fzf':
        selection = launchers.fzf(frequent)
    if args.command == 'game':
        selection = args.arguments[0]

    cache(selection)

    # Get config for game
    game_config = config["games"][selection]

    # Set wine executable
    if "wine" in game_config:
        wine = os.path.expanduser(game_config["wine"])
    else:
        wine = os.path.expanduser(config["wine"])

    if "env" in config:
        env.update(config["env"])

    # Set wine prefix
    if "prefix" in game_config:
        env["WINEPREFIX"] = os.path.expanduser(game_config["prefix"])
    else:
        env["WINEPREFIX"] = os.path.expanduser(config["prefix"])

    mangoapp = get_value(config, game_config, 'mangoapp')
    mangohud = get_value(config, game_config, 'mangohud')
    gamescope = get_value(config, game_config, 'gamescope')
    print(
        f'mangoapp: {mangoapp}, mangohud: {mangohud}, gamescope: {gamescope}')

    # Set MANGOHUD environment variable
    if mangohud and not mangoapp:
        env["MANGOHUD"] = "1"

    base_command = [wine, os.path.expanduser(game_config["exe"])]
    if gamescope:
        command = [
            "gamescope", "-h", "1440", "-H", "1440",
            "--backend=sdl", "-f", "--"]
        if mangoapp:
            command.insert(1, '--mangoapp')
        command = command + base_command
    else:
        command = base_command

    # Execute command
    Popen(command, env=env)


if __name__ == "__main__":
    main()
