import struct
from bitarray.util import *
from bitarray import bitarray, decodetree
from arc import Arc
import sys
import argparse
import os

parser = argparse.ArgumentParser(description='Insert folder\'s content to arc archive')
parser.add_argument('folder_path', type=str, help='Path to the folder have modded file')
parser.add_argument('arc_path', type=str, help='Path to the .arc file')
parser.add_argument('out_path', type=str, help='Path to output .arc file')
args = parser.parse_args()
folder_path = args.folder_path
arc_path = args.arc_path
out_path = args.out_path

################ read
with open(arc_path,"rb") as f:
    raw = f.read()
data = Arc.from_bytes(raw)

filenames = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))] 

filemod = []
diffmod = []
diff = 0
for file in data.files:
    diffmod.append(diff)
    name = file.file_name.rstrip("\x00")
    if name in filenames:
        with open(os.path.join(folder_path, name), 'rb') as f:
            newraw = f.read()
            filemod.append(newraw)
        diff += len(newraw) - file.len_data
    else: 
        filemod.append(False)

f = open(out_path,"wb")
f.write(data.magic)
f.write(struct.pack("<I",data.num_files))
for i, file in enumerate(data.files):
    f.write(file.file_name.encode('utf-8').ljust(0x60,b'\x00'))
    f.write(struct.pack("<I",file.offset + diffmod[i]))
    f.write(struct.pack("<I",len(filemod[i]) if filemod[i] else file.len_data))
    f.write(file.skip)

for i, file in enumerate(data.files):
    f.write(filemod[i] if filemod[i] else file.data.file_content)
