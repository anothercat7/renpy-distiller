import abc
import os
import posixpath
import zipfile

class Base(abc.ABC):
    """The base class for all readers and writers."""

    @abc.abstractmethod
    def __enter__(self):
        pass

    @abc.abstractmethod
    def __exit__(self, *args):
        pass

    @abc.abstractmethod
    def __truediv__(self, path):
        pass

    @abc.abstractmethod
    def close(self):
        """Close the reader/writer."""
        pass

    @abc.abstractmethod
    def get_name(self):
        """Get the filename component of the path."""
        pass

    @abc.abstractmethod
    def with_name(self, name):
        """Create a reader/writer for the given filename."""
        pass

class BaseReader(abc.ABC):
    """A mix-in base class for readers."""

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def is_dir(self):
        """Test if the path exists and is a directory."""
        pass

    @abc.abstractmethod
    def is_file(self):
        """Test if the path exists and is a normal file."""
        pass

    @abc.abstractmethod
    def read(self):
        """Read a file."""
        pass

    @abc.abstractmethod
    def stat(self):
        """Find the mode bits of a file."""
        pass

class BaseWriter(abc.ABC):
    """A mix-in base class for readers."""

    @abc.abstractmethod
    def mkdir(self, mode):
        """Create a directory."""

    @abc.abstractmethod
    def write(self, data, mode):
        """Create a file."""

class FileBase(Base):
    """The base class for directory readers and writers."""

    __slots__ = [
        '_path'
    ]

    def __init__(self, path):
        self._path = path.removesuffix('/')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __repr__(self):
        return f'{type(self).__name__}({repr(self._path)})'

    def __truediv__(self, path):
        return type(self)(os.path.join(self._path, path))

    def close(self):
        pass

    def get_name(self):
        return os.path.basename(self._path)

    def with_name(self, name):
        return type(self)(os.path.join(os.path.dirname(self._path), name))

class FileReader(FileBase, BaseReader):
    """An abstraction for reading files from a directory."""

    __slots__ = []

    def __iter__(self):
        class FileReaderIterator:
            __slots__ = [
                '_names',
                '_reader'
            ]

            def __init__(self, reader):
                self._reader = reader
                self._names = iter(os.listdir(reader._path))

            def __next__(self):
                return self._reader / next(self._names)

        return FileReaderIterator(self)

    def is_dir(self):
        return os.path.isdir(self._path)

    def is_file(self):
        return os.path.isfile(self._path)

    def read(self):
        with open(self._path, 'rb') as file:
            return file.read()

    def stat(self):
        return os.stat(self._path).st_mode

class FileWriter(FileBase, BaseWriter):
    """An abstraction for writing files to a directory."""

    __slots__ = []

    def mkdir(self, mode):
        os.makedirs(self._path, mode, True)
        os.chmod(self._path, mode)

    def write(self, data, mode):
        os.makedirs(os.path.dirname(self._path), 0o777, True)
        with open(self._path, 'wb') as file:
            file.write(data)
        os.chmod(self._path, mode)

class ZipBase(Base):
    """The base class for zip file readers and writers."""

    __slots__ = [
        '_names',
        '_path',
        '_zip'
    ]

    def __init__(self, path, mode = None, zip = None, names = None):
        if zip is None:
            self._names = None
            self._path = ''
            self._zip = zipfile.ZipFile(path, mode)
        else:
            self._names = names
            self._path = path.removesuffix('/')
            self._zip = zip

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        path = repr(os.path.join(self._zip.filename, self._path))
        return f'{type(self).__name__}({path})'

    def __truediv__(self, path):
        return type(self)(
            posixpath.join(self._path, path),
            self._zip,
            self._names
        )

    def close(self):
        self._zip.close()

    def get_name(self):
        return posixpath.basename(self._path)

    def with_name(self, name):
        return type(self)(
            posixpath.join(posixpath.dirname(self._path), name),
            self._zip,
            self._names
        )

class ZipReader(ZipBase, BaseReader):
    """An abstraction for reading files from a Zip file."""

    __slots__ = []

    def __init__(self, path, *args):
        super().__init__(path, 'r', *args)

        # Build a list of all file and directory names.  We have to do this
        # since Zip files often do not explicitly include entries for all
        # of the directories in them.
        if not self._names:
            self._names = set()

            for info in self._zip.filelist:
                name = info.filename

                # Make sure directory names always end with a slash and
                # normal filenames never end with a slash.  We depend on
                # this in is_dir and is_file.
                if info.is_dir():
                    if not name.endswith('/'):
                        name += '/'
                else:
                    name = name.removesuffix('/')

                self._names.add(name)

                # Make sure all the parent directories are added.
                while '/' in name[:-1]:
                    name = name[:-1].rsplit('/', 1)[0] + '/'
                    self._names.add(name)

            self._names = sorted(self._names)

    def __iter__(self):
        class ZipReaderIterator:
            __slots__ = [
                '_names',
                '_reader'
            ]

            def __init__(self, reader):
                self._reader = reader
                self._names = iter(reader._names)

            def __next__(self):
                while True:
                    name = next(self._names).removesuffix('/')
                    if posixpath.dirname(name) == self._reader._path:
                        return self._reader / posixpath.basename(name)

        return ZipReaderIterator(self)

    def is_dir(self):
        return self._path + '/' in self._names

    def is_file(self):
        return self._path in self._names

    def read(self):
        return self._zip.read(self._path)

    def stat(self):
        if self.is_file():
            return self._zip.getinfo(self._path).external_attr >> 16
        if self.is_dir():
            return 0o755

class ZipWriter(ZipBase, BaseWriter):
    """An abstraction for writing files to a Zip file."""

    __slots__ = []

    def __init__(self, path, *args):
        super().__init__(path, 'w', *args)

    def mkdir(self, mode):
        self._zip.mkdir(self._path, mode)

    def write(self, data, mode):
        info = zipfile.ZipInfo(self._path)
        info.external_attr = mode << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        self._zip.writestr(info, data)

def copy(reader, writer):
    """Recursively copy from a file reader to a file writer."""
    if reader.is_dir():
        writer.mkdir(reader.stat())
        for file in reader:
            copy(file, writer / file.get_name())
    else:
        writer.write(reader.read(), reader.stat())

def reader(path):
    """Return a reader appropriate for the path."""
    if os.path.isfile(path):
        reader = ZipReader(path)

        # Zipped Ren'Py SDKs and games usually have everything inside a
        # top-level directory; enter that directory if it exists.
        files = list(reader)
        if len(files) == 1 and files[0].is_dir():
            reader = files[0]

        return reader
    else:
        return FileReader(path)

def writer(path):
    """Return a writer appropriate for the path."""
    if path.lower().endswith('.zip'):
        writer = ZipWriter(path)

        # Zipped Ren'Py games usually have everything inside a top-level
        # directory; use the name of the Zip file as the name of that
        # directory.
        writer /= os.path.basename(path)[:-len('.zip')]

        return writer
    else:
        return FileWriter(path)
