import pathlib

from . import files

class GameAnalyzer:
    """Analyzer for a Ren'Py game.

    A GameAnalyzer determines whether or not a directory contains a valid
    Ren'Py game; it also stores some basic information about the game.
    """

    __slots__ = [
        'name',
        'path',
        'valid'
    ]

    def __init__(self, path):
        self.path = path
        with files.reader(path) as reader:
            self._analize(reader)

    def _analize(self, reader):
        self.name = None
        self.valid = True

        for dir in ('lib', 'game', 'renpy'):
            if not (reader / dir).is_dir():
                self.valid = False
                return

        # Look at the custom-named executables found in the top level
        # directory of the Ren'Py game to determine its name; these
        # executables must be consistently named.  We try to ignore
        # extraneous executables.
        py = set()
        sh = set()
        exe = set()

        for file in reader:
            for names, suffix in ((py, '.py'), (sh, '.sh'), (exe, '.exe')):
                if file.get_name().endswith(suffix):
                    names.add(file.get_name().removesuffix(suffix))
                    break

        names = py | sh | exe
        if py:
            names &= py
        if sh:
            names &= sh
        if exe:
            names &= exe

        if len(names) != 1:
            self.valid = False
            return

        self.name = list(names)[0]

class SDKAnalyzer:
    """Analyzer for a Ren'Py SDK.

    An SDKAnalyzer determines whether or not a directory contains a valid
    Ren'Py SDK; it also stores some basic information about the SDK.
    """

    __slots__ = [
        'path',
        'valid'
    ]

    def __init__(self, path):
        self.path = path
        with files.reader(path) as reader:
            self._analize(reader)

    def _analize(self, reader):
        self.valid = True

        for dir in ('lib', 'renpy'):
            if not (reader / dir).is_dir():
                self.valid = False
                return

        for file in ('renpy.exe', 'renpy.py', 'renpy.sh'):
            if not (reader / file).is_file():
                self.valid = False
                return

class OutputAnalyzer:
    """Analyzer for a potential output directory.

    An OutputAnalyzer determines whether or not an output directory is
    valid; it also extracts some basic information about the output
    directory.
    """

    __slots__ = [
        'empty',
        'path',
        'valid'
    ]

    def __init__(self, path):
        self.path = path
        self._analize(pathlib.Path(path))

    def _analize(self, path):
        self.valid = True
        self.empty = True

        if path.exists():
            if path.is_dir():
                self.empty = not list(path.iterdir())
            else:
                self.empty = False
            return

        # If the output path does not exist, the first parent which does
        # exist needs to be a directory so we can create the path.
        for parent in path.parents:
            if parent.exists():
                self.valid = parent.is_dir()
                return
