# Ren'Py Distiller API Documentation

This document describes Ren'Py Distiller's API, available through the
`renpy_distiller` package.

## Overview

The API is split into two modules: `analyzer` and `distiller`.  These are
*not* automatically imported when the `renpy_distiller` package is
imported; they must be imported explicitly:

```python
from renpy_distiller import analyzer, distiller
```

The `analyzer` module contains classes used to analyze Ren'Py games, SDKs,
and output paths; effectively, these analyzers try to verify that the
components are indeed what they seem to be.  They also collect and store
some information needed by the distiller.

The `distiller` module contains a class used to "distill" a Ren'Py game —
that is, to create a new game by combining the original game's script with
various engine files from the SDK.  The distiller relies on information
collected by the analyzers.

Note that the `renpy_distiller` package also includes the modules `cli` and
`files`; these are not part of the public API and may be changed or removed
without warning.

## Analyzer Module

The `analyzer` module contains three classes: `GameAnalyzer`,
`SDKAnalyzer`, and `OutputAnalyzer`.  The constructor of each analyzer
class takes a single argument: the path to the directory or Zip file to be
analyze.  For example:

```python
from renpy_distiller import analyzer

game = GameAnalyzer('renpy-game.zip')
```

Each analyzer class performs its analysis when it is constructed.

If the path passed to `GameAnalyzer` or `SDKAnalyzer` points to a normal
file, that file is assumed to be a Zip file. This will result in
`zipfile.BadZipFile` being raised if the file is not in fact a valid Zip
file.

`OutputAnalyzer` does not attempt to open Zip files, so it will never raise
this exception.

### GameAnalyzer

A `GameAnalyzer` analyzes a Ren'Py game and tries to determine whether or
not it is valid.

#### `__init__(path)`

Construct the analyzer and analyze the game at the given path.

#### `name`

The name associated with the game's custom-named executables.  These are
files of the form `name.py`, `name.sh`, and `name.exe` in the top-level
directory of them game; these names also appear in some files in `lib/`.

#### `path`

The path to the game; this is the same as the path passed to the
constructor.

#### `valid`

True if the game seems to be valid.

### SDKAnalyzer

An `SDKAnalyzer` analyzes a Ren'Py SDK and tries to determine whether or
not it is valid.

#### `__init__(path)`

Construct the analyzer and analyze the SDK at the given path.

#### `path`

The path to the SDK; this is the same as the path passed to the
constructor.

#### `valid`

True if the SDK seems to be valid.

### OutputAnalyzer

An `OutputAnalyzer` analyzes an output path and tries to determine whether
or not it is valid

#### `__init__(path)`

Construct the analyzer and analyze the given output path.

#### `empty`

True if the output path is empty.  It is considered empty if it either does
not exist or points to an empty directory.

#### `path`

The output path; this is the same as the path passed to the constructor.

#### `valid`

True if the output path seems to be valid.  This is independent of whether
or not the path is empty.

## Distiller Module

The `distiller` module contains the `Distiller` class.  Its constructor
takes a `GameAnalyzer`, `SDKAnalyzer`, and `OutputAnalyzer` as its
arguments, which it then uses to distill the game.  For example:

```python
from renpy_distiller import analyzer, distiller

game = analyzer.GameAnalyzer('renpy-game.zip')
sdk = analyzer.SDKAnalyzer('renpy-sdk.zip')
output = analyzer.OutputAnalyzer('output.zip')

distiller.Distiller(game, sdk, output).distill()
```

Distillation does *not* automatically occur when a `Distiller` is
constructed; it must be triggered by calling the `distill()` method.

### Distiller

A `Distiller` performs the distillation process: it copies the `game/`
directory from the original game along with several files and directories
from the SDK into a new Zip file or directory.

#### `__init__(game, sdk, output)`

Construct the distiller with the given `GameAnalyzer`, `SDKAnalyzer`, and
`OutputAnalyzer`.

#### `distill()`

Distill the game.  This implicitly uses the information in the analyzers
that were passed to the constructor.
