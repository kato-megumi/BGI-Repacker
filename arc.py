# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Arc(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(12)
        if not self.magic == b"\x42\x55\x52\x49\x4B\x4F\x20\x41\x52\x43\x32\x30":
            raise kaitaistruct.ValidationNotEqualError(b"\x42\x55\x52\x49\x4B\x4F\x20\x41\x52\x43\x32\x30", self.magic, self._io, u"/seq/0")
        self.num_files = self._io.read_u4le()
        self.files = []
        for i in range(self.num_files):
            self.files.append(Arc.FileEntry(self._io, self, self._root))


    class FileEntry(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_name = (self._io.read_bytes(96)).decode(u"UTF-8")
            self.offset = self._io.read_u4le()
            self.len_data = self._io.read_u4le()
            self.skip = self._io.read_bytes(24)

        @property
        def data(self):
            if hasattr(self, '_m_data'):
                return self._m_data

            io = self._root._io
            _pos = io.pos()
            io.seek(((self.offset + 16) + (128 * self._root.num_files)))
            self._raw__m_data = io.read_bytes(self.len_data)
            _io__raw__m_data = KaitaiStream(BytesIO(self._raw__m_data))
            self._m_data = Arc.Bgi(_io__raw__m_data, self, self._root)
            io.seek(_pos)
            return getattr(self, '_m_data', None)


    class Bgi(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.file_content = self._io.read_bytes_full()



