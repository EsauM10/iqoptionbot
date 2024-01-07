import argparse
from iqoptionbot.app import run_app

global_parser = argparse.ArgumentParser(prog='iqoptionbot')
subparsers    = global_parser.add_subparsers(title='commands')

def main():
    subparsers.add_parser('run', help='runs iqoption bot').set_defaults(func=run_app)
    args = global_parser.parse_args()
    args.func()
