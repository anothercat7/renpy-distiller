from pathlib import Path

class GameAnalizer:
    """Analizer for a Ren'Py game.

    A GameAnalizer determines whether or not a directory contains a valid
    Ren'Py game; it also stores some basic information about the game.
    """

    __slots__ = [
        'name',
        'path',
        'valid'
    ]

    def __init__(self, path):
        self.path = Path(path)
        self._analize()

    def _analize(self):
        self.name = None
        self.valid = True

        for dir in ('lib', 'game', 'renpy'):
            if not (self.path / dir).is_dir():
                self.valid = False
                return

        # Look at the custom-named executables found in the top level
        # directory of the Ren'Py game to determine its name; these
        # executables must be consistently named.  We try to ignore
        # extraneous executables.
        names = set()
        for suffix in ('.exe', '.py', '.sh'):
            match = set(file.name.removesuffix(suffix) \
                        for file in self.path.glob('*' + suffix))
            if match:
                if names:
                    names &= match
                else:
                    names = match

        if len(names) != 1:
            self.valid = False
            return

        self.name = list(names)[0]

class SDKAnalizer:
    """Analizer for a Ren'Py SDK.

    An SDKAnalizer determines whether or not a directory contains a valid
    Ren'Py SDK; it also stores some basic information about the SDK.
    """

    __slots__ = [
        'path',
        'valid'
    ]

    def __init__(self, path):
        self.path = Path(path)
        self._analize()

    def _analize(self):
        self.valid = True

        for dir in ('lib', 'renpy'):
            if not (self.path / dir).is_dir():
                self.valid = False
                return

        for file in ('renpy.exe', 'renpy.py', 'renpy.sh'):
            if not (self.path / file).is_file():
                self.valid = False
                return

class OutputAnalizer:
    """Analizer for a potential output directory.

    An OutputAnalizer determines whether or not an output directory is
    valid; it also extracts some basic information about the output
    directory.
    """

    __slots__ = [
        'empty',
        'path',
        'valid'
    ]

    def __init__(self, path):
        self.path = Path(path)
        self._analize()

    def _analize(self):
        self.valid = True
        self.empty = True

        if self.path.exists() and not self.path.is_dir():
            self.valid = False
            return

        if not self.path.exists():
            for parent in self.path.parents:
                if parent.exists() and not parent.is_dir():
                    self.valid = False
                    return

        if self.path.exists():
            self.empty = not list(self.path.iterdir())
