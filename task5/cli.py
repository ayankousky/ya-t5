"""
task5

Usage:
  task5 hello
  task5 reqstat
  task5 sizestat
  task5 -h | --help
  task5 --version
  task5 regularbyuser -f <csv_file_path> [--src_user <src_user>] [--src_ip <src_ip>] [--period <period in minutes>] [--duration <csv duration>] [--min_repeats <min request repeats>] [--empty]

Options:
  -h --help                                     Show this screen.
  --version                                     Show version.
  -f <csv_file_path>                            Path to the journal. Required
  --src_user <src_user>                         Filter for src_user. Default: none (all entries in journal)
  --src_ip <src_ip>                             Filter for src_ip. Default: none (all entries in journal)
  --period <period>                             CSV export period in minutes. Default: 1440 min (24h)
  --duration <duration in minutes>              How long the regular requests should last. Entries should be repeated in this period <min_repeats> times. Default: 120 min
  --min_repeats <count>                         A minimum count of entries should be found to proceed in specified duration. Default: 8
  --empty                                       Including empty (src_user or src_ip)

Examples:
  task5 hello
  task5 reqstat
  task5 sizestat
  task5 regularbyuser
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
