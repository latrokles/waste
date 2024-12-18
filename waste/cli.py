import click

from waste.aidem import aidem
from waste.archivist import archivist
from waste.doodle import doodle
from waste.gui import gui_test
from waste.melody import melody
from waste.nabu import nabu
from waste.scowl import scowl
from waste.scribe import scribe


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


cli.add_command(aidem)
cli.add_command(archivist)
cli.add_command(doodle)
cli.add_command(melody)
cli.add_command(nabu)
cli.add_command(scowl)
cli.add_command(scribe)
cli.add_command(gui_test)
