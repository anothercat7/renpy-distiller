# Ren'Py Distiller

Ren'Py Distiller is a library and command-line tool for replacing the
engine files in an exported Ren'Py game with clean versions from the Ren'Py
SDK.  This of course begs the question: why would you want to do that?
Well, for starters, you can:

- Upgrade a Ren'Py game to use a later (or earlier) version of Ren'Py.

- Ensure the engine code in a Ren'Py game does not have viruses or malware
  attached to it.  *(Note that this does not address the possibility of the
  game script itself being infected.)*

- Undo any alterations the game developer might have made to the Ren'Py
  engine itself.

You can probably think of even more uses for it if you try!  (Or maybe
not...)

Ren'Py Distiller is primarily intended for players, not developers; when
developing a Ren'Py game, tasks such as upgrading the version of Ren'Py
used in the game are much better handled via the normal SDK upgrade method.

## Usage

In order to use Ren'Py Distiller, you need two things:

- A Ren'Py game (these can be found on https://itch.io and elsewhere)

- A copy of the Ren'Py SDK (which can be downloaded from https://renpy.org)

Ren'Py games and the Ren'Py SDK are normally distributed in Zip files.  You
can extract the game and SDK, or you can leave them as Zip files; Ren'Py
Distiller can handle both.

Once you have a game and a copy of the SDK, run:

```sh
renpy-distiller renpy-game.zip -s renpy-sdk.zip -o output.zip
```

or:

```sh
renpy-distiller renpy-game/ -s renpy-sdk/ -o output/
```

This copies the game to the specified output directory or Zip file,
replacing all of the engine files with clean versions from the SDK.  Note
that Ren'Py Distiller refuses to overwrite existing Zip files and nonempty
directories.

See the [CLI documentation](doc/cli.md) for more information.

## API

You can also use Ren'Py Distiller programmatically:

```python
from renpy_distiller import analyzer, distiller

game = analyzer.GameAnalyzer('renpy-game.zip')
sdk = analyzer.SDKAnalyzer('renpy-sdk.zip')
output = analyzer.OutputAnalyzer('output.zip')

distiller.Distiller(game, sdk, output).distill()
```

See the [API documentation](doc/api.md) for more information.

## Limitations

- Only Ren'Py games exported for Linux and Windows are supported; games
  exported for macOS, iOS, Android, and web platforms are not supported.

- Only Ren'Py 6.15.0 and later versions are supported; this applies both to
  the game and the SDK.

- Games which depend on files outside of the `game/` directory will break.

- Downgrading a game is likely to break it; upgrading a game across many
  major versions of the SDK might break it.

- If a game only supplies the script in bytecode form, it will break unless
  you use an SDK version which is bytecode-compatible with the SDK version
  used to export the game.

## Bugs

Ren'Py Distiller probably has various bugs.  Please report them if you come
across any!
