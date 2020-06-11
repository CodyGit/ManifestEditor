#!/usr/bin/python3
#coding=utf-8
#author: cody

from ManifestEditor.BaseChunk import BaseChunk
from ManifestEditor.Util import *

"""
Chunk Type : 4 bytes，始终为 0x001c0001，标记这是 String Chunk
Chunk Size : 4 bytes，表示 String Chunk 的大小
String Count : 4 bytes，表示字符串的数量
Style Count : 4 bytes，表示样式的数量
Unkown : 4 bytes,固定值，0x00000000
String Pool Offset : 字符串池的偏移量，注意不是相对于文件开始处，而是相对于 String Chunk 的开始处
Style Pool Offset : 样式池的偏移量，同上，也是相对于 String Chunk 而言
String Offsets : int数组，大小为 String Count，存储每个字符串在字符串池中的相对偏移量
Style Offets : 同上，也是 int 数组。总大小为 Style Count * 4 bytes
String Pool : 字符串池，存储了所有的字符串
Style Pool : 样式池，存储了所有的样式
"""
class StringChunk(BaseChunk):
    def __init__(self, all_bytes, offset):
        BaseChunk.__init__(self, all_bytes, offset)
        # 因为父类处理了chunk_type 和 chunk_size，所以从 8 开始
        reader = create_reader(self.byte_arr, 8)
 
        self.string_count = bytes_to_int(reader(4))
        self.style_count = bytes_to_int(reader(4))

        #unknow 4bytes
        reader(4)

        self.string_pool_offset = bytes_to_int(reader(4))
        self.style_pool_offset = bytes_to_int(reader(4))

        self.string_offsets = []
        self.string_value_arr = []
        count = 0 
        while(count < self.string_count):
            b = reader(4)
            offset = bytes_to_int(b)
            self.string_offsets.append(offset)
            str_val = self._transform(self.string_pool_offset + offset)
            self.string_value_arr.append(str_val)
            count = count + 1
        
        self.style_offsets = []
        self.style_value_arr = []

        count = 0 
        while(count < self.style_count):
            offset = bytes_to_int(reader(4))
            self.style_offsets.append(offset)
            sty_val = self._transform(self.style_pool_offset + offset)
            self.style_arr.append(sty_val)
            count = count + 1

    def _transform(self, offset):
        cursor = offset
        next_cursor = cursor + 2
        # 开头两个字节表示字符串长度
        str_len = bytes_to_int(self.byte_arr[cursor:next_cursor])
        cursor = next_cursor

        # str_len * 2
        next_cursor = cursor + str_len*2
        value = self.byte_arr[cursor:next_cursor].decode("utf-16")
        cursor = next_cursor
        return value
    
    """
    @index string_arr 的下标
    @new_str 新的值
    TODO
    """
        
    def modify(self, index, new_str):
        old_str = self.string_value_arr[index]
        if old_str == new_str:
            return
        new_len = len(new_str)
        old_len = len(old_str)
        # 前两位是字符串长度
        new_byte_arr = bytearray(int_to_bytes(new_len, 2))
        delta = (new_len - old_len)*2
        new_byte_arr.extend(new_str.encode("utf-16")[2:])

        # 找到被修改字符串所在的位置
        offset = self.string_offsets[index] + self.string_pool_offset
        # 一个字符是两个字节，头上两个字节表示长度
        self.replace_bytes(new_byte_arr, offset, old_len*2 + 2)
        # 字符串长度发生变化
        # 需要修改StringChunk的 chunk_size
        # 需要修改排在该字符串后面的 string_offset
        # 被修改字符串的长度
        # TODO style pool 要不要调整？目前的测试数据里style pool总是空，这里可能有Bug
        if delta != 0:
            self.chunk_size = self.chunk_size + delta
            if index + 1 < self.string_count:
                offset_byte_arr = bytearray()
                for i in range(index+1, self.string_count):
                    new_offset = self.string_offsets[i] + delta
                    self.string_offsets[i] = new_offset
                    offset_byte_arr.extend(int_to_bytes(new_offset))
                self.replace_bytes(offset_byte_arr, 4*7+index*4 + 4)
            # 因为字符串修改是是以两个字节位单位添加的，会导致chunk的4字节对齐被打乱，需要补充0x0000
            if self.chunk_size % 4 != 0:
                # 尾端已经有多余的0x0000
                if bytes_to_int(self.byte_arr[-4:]) == 0:
                    self.byte_arr = self.byte_arr[:-2]
                    self.chunk_size  = self.chunk_size - 2
                else:
                    self.byte_arr.extend(int_to_bytes(0)[:2])
                    self.chunk_size  = self.chunk_size + 2
            self.replace_bytes(int_to_bytes(self.chunk_size), 4)
    """
    新增
    TODO
    """
    def add(self, new_str):
        pass
    
    def print_info(self):
        print("==StringChunk==")
        print("chunk_type:", self.chunk_type)
        print("chunk_size:", self.chunk_size)
        print("string count:", self.string_count)
        print("string pool offset:", self.string_pool_offset)
        print("string pool:")
        for v in self.string_value_arr:
            print(" "*4, self.string_value_arr.index(v), v)
        print("style count:", self.style_count)
        print("style pool offset:", self.style_pool_offset)
        print("style pool:")
        for v in self.style_value_arr:
            print(" "*4, self.style_value_arr.index(v), v)