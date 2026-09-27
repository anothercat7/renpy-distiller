# Ren'Py Distiller CLI Documentation

This document describes Ren'Py Distiller's CLI, available through the
`renpy-distiller` command.

## Invocation

The basic syntax of the `renpy-distiller` command is:

```sh
renpy-distiller GAME -s SDK -o OUTPUT
```

Where `GAME` is the path to the original Ren'Py game, `SDK` is the path to
the Ren'Py SDK, and `OUTPUT` is the output path.  Each of these paths may
point to either a directory or a Zip file.

Ren'Py distiller refuses to overwrite existing Zip files and nonempty
directories; `OUTPUT` should point either to an empty or nonexistent
directory or to a nonexistent Zip file.

## Options

Several option flags are available which modify the behavior of Ren'Py
Distiller.  We have already seen the `-s` and `-o` options, used to specify
the SDK and output paths; a full list of options follows.

### `-s, --sdk PATH`

Specify the path to the Ren'Py SDK.  The SDK may be either a directory or a
Zip file.  *This option is required.*

### `-o, --output PATH`

Specify the output path.  The output path may be either a directory or a
Zip file.  *This option is required.*

### `--help`

Show a brief summary of these options.

### `--version`

Show the Ren'Py Distiller version.

## Zip Support

Ren'Py Distiller supports reading games and the SDK from Zip files, and it
supports writing distilled games back to Zip files.  Conventionally, zipped
games and SDKs are contained in a top-level directory inside the Zip file.
For example, `my-game.zip` might contain:

```
my-game/
  my-game.exe
  my-game.py
  my-game.sh
  game/
    script.rpy
    ...
```

When reading games and SDKs from Zip files, such top-level directories are
automatically detected and handled.  When writing distilled games to Zip
files, a top-level directory with the same name as the Zip file is
automatically created.
