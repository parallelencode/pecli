#!/usr/bin/env python3

from cli.config import conf
from Startup.validation import validate_inputs
from Startup.startup import startup_check
from parallelencode import run
from cli.arg_parse import arg_parsing, convert_args
from cli.handle_callbacks import add_callbacks
from cli.logger import set_log


class pecli:
    """pecli - parallel encode command line interface for AV1, VP9, VP8 encoding"""
    def __init__(self):
        self.args = arg_parsing()

    def main_thread(self):
        """Main."""
        startup_check(self.args)
        conf(self.args)
        validate_inputs(self.args)
        c = add_callbacks(self.args)
        set_log(self.args["logging"], self.args["temp"])
        run(convert_args(self.args), c)


def main():
    pecli().main_thread()


if __name__ == '__main__':
    main()
