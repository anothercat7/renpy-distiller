import sys
import zipfile

import click

from . import analizer, distiller

@click.command()
@click.argument(
    'game',
    type = click.Path(exists = True),
    help = "Game input directory or Zip file."
)
@click.option(
    '-s',
    '--sdk',
    type = click.Path(exists = True),
    required = True,
    help = "Ren'Py SDK directory or Zip file."
)
@click.option(
    '-o',
    '--output',
    type = click.Path(),
    required = True,
    help = "Game output directory or Zip file."
)
@click.version_option()
def cli(game, sdk, output):
    """Replace the engine files in an exported Ren'Py game."""
    try:
        game = analizer.GameAnalizer(game)
    except zipfile.BadZipFile:
        click.echo("No valid Ren'Py game could be found in:")
        click.echo("    " + click.format_filename(game))
        click.echo("""\
Ren'Py Distiller only supportes reading Ren'Py games from directories
and Zip files.""")
        sys.exit(1)
    if not game.valid:
        click.echo("No valid Ren'Py game could be found in:")
        click.echo("    " + click.format_filename(game.path))
        click.echo("""\
Note that Ren'Py Distiller only supports Ren'Py games exported for Linux
and Windows using Ren'Py 6.15.0 or later; games exported with earlier
versions may not be recognized.""")
        sys.exit(1)

    try:
        sdk = analizer.SDKAnalizer(sdk)
    except zipfile.BadZipFile:
        click.echo("No valid Ren'Py SDK could be found in:")
        click.echo("    " + click.format_filename(sdk))
        click.echo("""\
Ren'Py Distiller only supportes reading the Ren'Py SDK from directories
and Zip files.""")
        sys.exit(1)
    if not sdk.valid:
        click.echo("No valid Ren'Py SDK could be found in:")
        click.echo("    " + click.format_filename(sdk.path))
        click.echo("""\
Note that Ren'Py Distiller only supports Ren'Py 6.15.0 or later; earlier
SDK versions may not be recognized.""")
        sys.exit(1)

    output = analizer.OutputAnalizer(output)
    if not output.valid:
        click.echo("No valid output path could be created at:")
        click.echo("    " + click.format_filename(output.path))
        sys.exit(1)
    if not output.empty:
        click.echo("Files exist in the output path at:")
        click.echo("    " + click.format_filename(output.path))
        click.echo("The output path must be empty.")
        sys.exit(1)

    click.echo("Distilling " + game.name + "...")

    distiller.Distiller(game, sdk, output).distill()

    click.echo("Wrote the distilled game to:")
    click.echo("    " + click.format_filename(output.path))
