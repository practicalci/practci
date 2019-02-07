# -*- coding: utf-8 -*-

"""Console script for practci."""
import sys
import click
from practci.utils.options import MutuallyExclusiveOption


@click.command()
def main(args=None):
    """Console script for practci."""
    click.echo("Replace this message by putting your code into "
               "practci.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


@click.group('practci')
@click.version_option('1.0')
def cli():
    pass


@cli.group('config')
def config():
    pass

@config.command
def config_show():
    click.echo("showing: pito")

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
