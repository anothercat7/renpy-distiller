import sys

import click

from . import analizer, distiller

@click.command()
@click.argument(
    'game',
    type = click.Path(exists = True, file_okay = False),
    help = "Path to the game input directory."
)
@click.option(
    '-s',
    '--sdk',
    type = click.Path(exists = True, file_okay = False),
    required = True,
    help = "Path to the Ren'Py SDK directory."
)
@click.option(
    '-o',
    '--output',
    type = click.Path(file_okay = False),
    required = True,
    help = "Path to the game output directory."
)
@click.version_option()
def cli(game, sdk, output):
    """Replace the engine files in an exported Ren'Py game."""
    game = analizer.GameAnalizer(game)
    if not game.valid:
        click.echo("No valid Ren'Py game could be found in:")
        click.echo("    " + click.format_filename(game.path))
        click.echo("""\
Note that Ren'Py Distiller only supports Ren'Py games exported for Linux
and Windows using Ren'Py 6.15.0 or later; games exported with earlier
versions may not be recognized.""")
        sys.exit(1)

    sdk = analizer.SDKAnalizer(sdk)
    if not sdk.valid:
        click.echo("No valid Ren'Py SDK could be found in:")
        click.echo("    " + click.format_filename(sdk.path))
        click.echo("""\
Note that Ren'Py Distiller only supports Ren'Py 6.15.0 or later; earlier
SDK versions may not be recognized.""")
        sys.exit(1)

    output = analizer.OutputAnalizer(output)
    if not output.valid:
        click.echo("No valid output directory could be created at:")
        click.echo("    " + click.format_filename(output.path))
        sys.exit(1)
    if not output.empty:
        click.echo("Files exist in the output directory at:")
        click.echo("    " + click.format_filename(output.path))
        click.echo("The output directory must be empty.")
        sys.exit(1)

    click.echo("Distilling " + game.name + "...")

    distiller.Distiller(game, sdk, output).distill()

    click.echo("Wrote the distilled game to:")
    click.echo("    " + click.format_filename(output.path))
