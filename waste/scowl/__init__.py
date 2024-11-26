import click

from .runtime import Runtime


@click.command()
def scowl():
    Runtime().start()
