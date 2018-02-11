"""The hello command."""


from json import dumps

from .base import Base


class ReqStat(Base):
    """Say hello, world!"""

    def run(self):
        print('kekeke')
        # print('You supplied the following options:', dumps(self.options, indent=2, sort_keys=True))
