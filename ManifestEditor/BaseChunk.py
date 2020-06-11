#!/usr/bin/python3
#coding=utf-8
#author: cody

from ManifestEditor.Util import *
class BaseChunk:
    def __init__(self, all_bytes, offset):
        reader = create_reader(all_bytes, offset)
        self.chunk_type = bytes_to_hex(reader(4))
        self.chunk_size =bytes_to_int(reader(4))
        self.start_offset = offset
        self.end_offset = offset + self.chunk_size
        self.byte_arr = bytearray(all_bytes[self.start_offset:self.end_offset])

    """
    替换chunk对应位置的byte
    @new_byte_arr 新写入的byte
    @offset 插入点
    @byte_len 被替换的字节长度

    将原来byte_arr在offset:offset+byte_len截断
    byte_part1 + offset:offset_byte_len + byte_part2
    替换乘
    byte_part1 + new_byte_arr + byte_part2
    """
    def replace_bytes(self, new_byte_arr, offset, byte_len=None):
        if byte_len == None:
            byte_len = len(new_byte_arr)
        byte_part1 = self.byte_arr[:offset]
        byte_part2 = self.byte_arr[offset + byte_len:]
        byte_part1.extend(new_byte_arr)
        byte_part1.extend(byte_part2)
        self.byte_arr = byte_part1