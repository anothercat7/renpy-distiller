# Ren'Py Distiller

Ren'Py Distiller is a library and command-line tool for replacing the
engine files in an exported Ren'Py game with clean versions from the Ren'Py
SDK.  Possible uses for it include:

- Upgrading a Ren'Py game to use a later (or earlier) version of Ren'Py

- Ensuring the engine code in a Ren'Py game does not have viruses or
  malware attached to it *(note that this does not address the possibility
  of the game script itself being infected)*

- Undoing any alterations the game developer might have made to the Ren'Py
  engine itself

Ren'Py Distiller is primarily intended for players of Ren'Py games, not
developers; when developing a Ren'Py game, tasks such as upgrading the
version of Ren'Py used in the game are much better handled by upgrading the
Ren'Py SDK.

## Usage

In order to use Ren'Py Distiller, you need two things:

- A Ren'Py game

- A copy of the Ren'Py SDK (which can be downloaded from https://renpy.org)

Ren'Py games and the Ren'Py SDK are normally distributed in archives; you
must extract them into directories.  After extracting, run:

```sh
renpy-distiller --sdk path/to/sdk --output path/to/output path/to/game
```

This will copy the Ren'Py game to the specified output directory, replacing
all of the engine files with clean versions from the SDK.  If the output
directory does not exist, it will be created; if it already exists, it must
be empty.

## API

You can also use Ren'Py Distiller programmatically:

```python
from renpy_distiller import analizer, distiller

game = analizer.GameAnalizer('path/to/game')
sdk = analizer.SDKAnalizer('path/to/sdk')
output = analizer.OutputAnalizer('path/to/output')

distiller.Distiller(game, sdk, output).distill()
```

## Limitations

Only Ren'Py games exported for Linux and Windows are supported; games
exported for macOS, iOS, Android, and web platforms are not supported.

Only Ren'Py 6.15.0 and later versions are supported; this applies both to
the game and the SDK.

Replacing a game's Ren'Py engine with a different version could break it;
this is especially likely when downgrading or moving across major version
numbers.

Even if the exact same version of Ren'Py is used, the game could still
break if it depends on alterations or extensions to the Ren'Py engine
itself; Ren'Py Distiller is explicitly intended to remove such alterations
and extensions.
