from gdb import Gdb
import argparse
import numpy as np

u32 = np.uint32
u16 = np.uint16
u8 = np.uint8

class Decryptor:
    def __init__(self, key: u32, magic: tuple[u16, u16]) -> None:
        self.key = key
        self.magic = (magic[1] << 24) | (magic[0] << 16)

    def update_key(self) -> u8:
        v0 = (self.key & 0xFFFF) * 20021
        v1 = self.magic | (self.key >> 16)
        v1 = v1 * 20021 + self.key * 346
        v1 = (v1 + (v0 >> 16)) & 0xFFFF
        self.key = (v1 << 16) + (v0 & 0xFFFF) + 1
        return u8(v1 & 0xff)

if __name__ == "__main__": 

    parser = argparse.ArgumentParser(description='Extract .gdb file')
    parser.add_argument('gdb_path', type=str, help='Path to the .gdb file')
    args = parser.parse_args()

    gdb_path = args.gdb_path
    with open(gdb_path,"rb") as f:
        raw = f.read()
    data = Gdb.from_bytes(raw)

    decrypt_data = bytearray(data.data)
    decryptor = Decryptor(data.key, data.magic[:2])
    for i in range(len(decrypt_data)):
        decrypt_data[i] = (decrypt_data[i] - decryptor.update_key()) & 0xFF

    decompressed_data = bytearray()
    i = 0
    while i < data.len_data:
        if decrypt_data[i] & 0x80:
            code = decrypt_data[i] & 0x7F
            copy_bytes = (code >> 3) + 2
            win_pos = ((code & 0x07) << 8) | decrypt_data[i + 1] + 2
            # Copy data from the sliding window
            for j in range(copy_bytes):
                decompressed_data.append(decompressed_data[-win_pos])
            i += 2
        else:
            # Direct copy
            copy_bytes = decrypt_data[i] + 1
            i += 1
            decompressed_data+=decrypt_data[i:i+copy_bytes]
            i += copy_bytes

    if len(decompressed_data) != data.uncomprlen:
        raise Exception("Decompressed data size mismatch")

    with open(gdb_path + ".bin", "wb") as f:
        f.write(decompressed_data)