import os
import shutil

class Distiller:
    """Distiller for a Ren'Py game.

    A Distiller handles the process of replacing Ren'Py engine files.  It
    uses the information in a GameAnalizer, SDKAnalizer, and OutputAnalizer
    to find and copy the necessary files and directories.
    """

    __slots__ = [
        'game',
        'sdk',
        'output'
    ]

    def __init__(self, game, sdk, output):
        self.game = game
        self.sdk = sdk
        self.output = output

    def distill(self):
        """Perform the distillation process."""
        os.makedirs(self.output.path, exist_ok = True)

        shutil.copytree(self.game.path / 'game', self.output.path / 'game')

        for dir in ('lib', 'renpy'):
            shutil.copytree(self.sdk.path / dir, self.output.path / dir)

        for suffix in ('.exe', '.py', '.sh'):
            generic = 'renpy' + suffix
            named = self.game.name + suffix
            shutil.copy(self.sdk.path / generic, self.output.path / named)

        for file in self.output.path.glob('lib/*/renpy'):
            os.rename(file, file.with_name(self.game.name))

        for file in self.output.path.glob('lib/*/renpy.exe'):
            os.rename(file, file.with_name(self.game.name + '.exe'))
