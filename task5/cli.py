"""
task5

Usage:
  task5 hello
  task5 reqstat
  task5 -h | --help
  task5 --version

Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  task5 hello
  task5 reqstat

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/rdegges/task5-cli
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import task5.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(task5.commands, k) and v:
            module = getattr(task5.commands, k)
            task5.commands = getmembers(module, isclass)
            command = [command[1] for command in task5.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()
