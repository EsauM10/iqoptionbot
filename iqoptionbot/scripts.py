import os
import argparse
from pathlib import Path
import subprocess

from iqoptionbot.app import run_app
from iqoptionbot.version import VERSION

BASEDIR = str(Path(__file__).parent)
SPEC_FILE = os.path.join(BASEDIR, 'app.spec')

global_parser = argparse.ArgumentParser(prog='iqoptionbot')
subparsers    = global_parser.add_subparsers(title='commands')

def build():
    subprocess.call(['pyinstaller', SPEC_FILE])

def show_version():
    print(f'iqoptionbot: v{VERSION}')

def main():
    subparsers.add_parser('run', help='runs iqoption bot').set_defaults(func=run_app)
    subparsers.add_parser('build', help='builds the executable file').set_defaults(func=build)
    subparsers.add_parser('version', help='prints the version number and exit').set_defaults(func=show_version)

    args = global_parser.parse_args()
    args.func()
