#!/usr/bin/python3
#coding=utf-8
#author: cody

from ManifestEditor.BaseChunk import BaseChunk
from ManifestEditor.TypedValue import TypedValue
from ManifestEditor.Util import *

class XmlContentChunk(BaseChunk):
    START_NAMESPACE = "0x00100100"
    END_NAMESPACE = "0x00100101"
    START_TAG = "0x00100102"
    END_TAG = "0x00100103"
    TEXT = "0x00100104"
    def __init__(self, all_bytes, offset):
        cursor = offset
        all_chunk_size = len(all_bytes)
        self.chunk_arr = []
        self._tag_chunk_arr = {}
        self.chunk_size = 0
        while (cursor < all_chunk_size):
            chunk_type = bytes_to_hex(all_bytes[cursor: cursor + 4])
            chunk = None
            if chunk_type == self.START_NAMESPACE: 
                chunk = NamespaceChunk(all_bytes, cursor)
            elif chunk_type == self.END_NAMESPACE:
                chunk = NamespaceChunk(all_bytes, cursor)
            elif chunk_type == self.START_TAG:
                chunk = TagChunk(all_bytes, cursor)
                if not self._tag_chunk_arr.get(chunk.name):
                    self._tag_chunk_arr[chunk.name] = []
                self._tag_chunk_arr[chunk.name].append(chunk)
                chunk.parse_attribute()
            elif chunk_type == self.END_TAG:
                chunk = TagChunk(all_bytes, cursor)
            elif chunk_type == self.TEXT:
                chunk = TextChunk(all_bytes, cursor)
            else:
                break
            self.chunk_size = self.chunk_size + chunk.chunk_size
            self.chunk_arr.append(chunk)
            cursor = chunk.end_offset

    def find_tag_chunk(self, tag_name, attr_key = None, attr_value = None):
        if tag_name and self._tag_chunk_arr.get(tag_name):
            if attr_key:
                for chunk in self._tag_chunk_arr[tag_name]:
                    if chunk.query_attribute(attr_key, attr_value):
                        return chunk
            else:
                return self._tag_chunk_arr[tag_name][0]
        
class NamespaceChunk(BaseChunk):
    def __init__(self, all_bytes, offset):
        BaseChunk.__init__(self, all_bytes, offset)
        
        reader = create_reader(self.byte_arr, 8)

        self.line_number = bytes_to_int(reader(4))

        # unknow 4bytes
        reader(4)

        self.prefix = bytes_to_int(reader(4))
        self.uri = bytes_to_int(reader(4))


class TagChunk(BaseChunk):
    def __init__(self, all_bytes, offset):
        BaseChunk.__init__(self, all_bytes, offset)

        reader = create_reader(self.byte_arr, 8)

        self.line_number = bytes_to_int(reader(4))
        
        # unknow 4bytes
        reader(4)

        self.namespace_uri = bytes_to_int(reader(4))
        self.name = TypedValue.convertToString(bytes_to_int(reader(4)))

    def parse_attribute(self):
        # 前6个字节已经在构造函数中解析过了
        reader = create_reader(self.byte_arr, 4*6)
        self.flags = reader(4)
        self.attribute_count = bytes_to_int(reader(4))
        self.class_attribute = reader(4)

        # print("attr count:", self.attribute_count)
        count = 0
        """
        每个属性固定 20 个字节，包含 5 个字段，每个字段都是 4 字节无符号 int，各个字段含义如下：
        namespaceUri : 属性的命名空间 uri 在字符串池中的索引。此处很少会等于 -1
        name : 属性名称在字符串池中的索引
        valueStr : 属性值
        type : 属性类型
        data : 属性数据
        """
        key_arr = ["namespaceUri", "name", "valueStr", "type", "data"]
        self.attr_arr = []
        while(count < self.attribute_count):
            attr_dict = {}
            for i in range(5):
                b = reader(4)
                value = bytes_to_int(b)
                if i == 0: # namespaceUri
                    attr_dict[key_arr[i]] = TypedValue.convertToString(value)
                elif i == 1: # name
                    attr_dict[key_arr[i]] = TypedValue.convertToString(value)
                elif i == 2: # valueStr
                    attr_dict[key_arr[i]] = value
                elif i == 3: # type 这里为什么要右移24？
                    attr_dict[key_arr[i]] = value >> 24
                elif i == 4: # data
                    attr_dict[key_arr[i]] = TypedValue.coerceToString(attr_dict["type"], value)
                    attr_dict["data_orig"] = value
                else:
                    pass
            self.attr_arr.append(attr_dict)
            attr_dict["order"] = count
            count = count + 1

    def query_attribute(self, attr_key, attr_value):
        for attr in self.attr_arr:
            if attr["name"] == attr_key:
                if attr_value == None or attr_value == attr["data"]:
                    return attr
                else:
                    return None
        return None

    def get_attr_value(self, attr_key):
        attr_obj = self.query_attribute(attr_key, None)
        return attr_obj["data"]

    def modify(self, attr_key, attr_value):
        attr_dict = self.query_attribute(attr_key, None)
        # 如果是字符串类型只需要用索引去修改对应的StringChunk
        if attr_dict["type"] == TypedValue.TYPE_STRING:
            attr_dict["data"] = attr_value
            return True, attr_dict["data_orig"]
        else:
            # 偏移了 4 * 9 个字节
            # # index 第几个属性
            base_offset = 4*9 + 4*4
            t = type(attr_value)
            b = None
            # 判断 attr_value 的类型
            # 先把值转换成对应的bytes
            # 找到对应的位置替换
            if t  == int:
                b = int_to_bytes(attr_value)
            elif t == float:
                b = float_to_bytes(attr_value)
            self.replace_bytes(b, base_offset + attr_dict["order"] * 4 * 5)
            return False, None

    def print_info(self):
        for attr in self.attr_arr:
            for k in attr:
                print(" ", k, attr[k])
            print("====")




class TextChunk(BaseChunk):
    def __init__(self, all_bytes, offset):
        BaseChunk.__init__(self, all_bytes, offset)


        reader = create_reader(self.byte_arr, 8)

        self.line_number = bytes_to_int(reader(4))
        
        # unknow 4bytes
        reader(4)

        self.name = bytes_to_int(reader(4))