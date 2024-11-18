# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Gdb(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.magic = self._io.read_bytes(16)
        if not self.magic == b"\x53\x44\x43\x20\x46\x4F\x52\x4D\x41\x54\x20\x31\x2E\x30\x30\x00":
            raise kaitaistruct.ValidationNotEqualError(b"\x53\x44\x43\x20\x46\x4F\x52\x4D\x41\x54\x20\x31\x2E\x30\x30\x00", self.magic, self._io, u"/seq/0")
        self.key = self._io.read_u4le()
        self.len_data = self._io.read_u4le()
        self.uncomprlen = self._io.read_u4le()
        self.sum_check = self._io.read_u2le()
        self.xor_check = self._io.read_u2le()
        self.data = self._io.read_bytes(self.len_data)


