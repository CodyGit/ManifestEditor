#!/usr/bin/python3
#coding=utf-8
#author: cody

from ManifestEditor.StringChunk import StringChunk
from ManifestEditor.ResourceChunk import ResourceChunk
from ManifestEditor.XmlContentChunk import XmlContentChunk
from ManifestEditor.TypedValue import TypedValue
from ManifestEditor.Util import *
import os

class AndroidManifest:
    def __init__(self, xml_path):
        if not os.path.exists(xml_path):
            raise Exception("%s not exists"%(xml_path))
        with open(xml_path, 'rb') as input_stream:
            input_data = input_stream.read()
            self.magic_bytes = input_data[0:4]

            string_chunk = StringChunk(input_data, 8)
            TypedValue.setStringArr(string_chunk.string_value_arr)
            resource_chunk = ResourceChunk(input_data, string_chunk.end_offset)
            xml_chunk = XmlContentChunk(input_data, resource_chunk.end_offset)

            self.string_chunk = string_chunk
            self.resource_chunk = resource_chunk
            self.xml_chunk = xml_chunk
    
    def output_bytes(self, output_xml):
        with open(output_xml, 'wb') as output_stream:
            all_size = 8 + self.string_chunk.chunk_size + self.resource_chunk.chunk_size + self.xml_chunk.chunk_size
            output_stream.write(self.magic_bytes)
            output_stream.write(int_to_bytes(all_size))
            output_stream.write(self.string_chunk.byte_arr)
            output_stream.write(self.resource_chunk.byte_arr)
            for chunk in self.xml_chunk.chunk_arr:
                output_stream.write(chunk.byte_arr)

