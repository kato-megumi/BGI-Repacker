meta:
  id: arc
  file-extension: arc
  endian: le
seq:
  - id: magic
    contents:
      - 'BURIKO ARC20'
  - id: num_files
    type: u4
  - id: files
    type: file_entry
    repeat: expr
    repeat-expr: num_files
types:
  file_entry:
    seq:
      - id: file_name
        type: str
        size: 0x60
        encoding: UTF-8
      - id: offset
        type: u4
      - id: len_data
        type: u4
      - id: skip
        size: 0x18
    instances:
      data:
        pos: offset + 0x10 + 0x80 * _root.num_files
        size: len_data
        type: bgi
        io: _root._io
  bgi:
    seq:
      - id: file_content
        size-eos: True

