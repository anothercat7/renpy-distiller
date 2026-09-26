from . import files

class Distiller:
    """Distiller for a Ren'Py game.

    A Distiller handles the process of replacing Ren'Py engine files.  It
    uses the information in a GameAnalizer, SDKAnalizer, and OutputAnalizer
    to find and copy the necessary files and directories.
    """

    __slots__ = [
        '_game',
        '_sdk',
        '_output'
    ]

    def __init__(self, game, sdk, output):
        self._game = game
        self._sdk = sdk
        self._output = output

    def distill(self):
        """Perform the distillation process."""
        game = files.reader(self._game.path)
        sdk = files.reader(self._sdk.path)
        output = files.writer(self._output.path)

        files.copy(game / 'game', output / 'game')
        files.copy(sdk / 'renpy', output / 'renpy')

        # Some files in lib need to have a customized name, similar to
        # renpy.exe and friends in the top-level directory.  This function
        # helps copy lib while renaming these files.
        def copy_lib(reader, writer):
            if reader.is_dir():
                writer.mkdir(reader.stat())
                for file in reader:
                    copy_lib(file, writer / file.get_name())
            else:
                if writer.get_name() == 'renpy':
                    writer = writer.with_name(self._game.name)
                if writer.get_name() == 'renpy.exe':
                    writer = writer.with_name(self._game.name + '.exe')
                writer.write(reader.read(), reader.stat())

        copy_lib(sdk / 'lib', output / 'lib')

        for suffix in ('.exe', '.py', '.sh'):
            generic = 'renpy' + suffix
            named = self._game.name + suffix
            files.copy(sdk / generic, output / named)

        game.close()
        sdk.close()
        output.close()
