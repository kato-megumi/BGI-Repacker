meta:
  id: gdb
  file-extension: gdb
  endian: le
seq:
  - id: magic
    contents:
      - 'SDC FORMAT 1.00'
      - 0x00
  - id: key
    type: u4
  - id: len_data
    type: u4
  - id: uncomprlen
    type: u4
  - id: sum_check
    type: u2
  - id: xor_check
    type: u2
  - id: data
    size: 'len_data'