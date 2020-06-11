#!/usr/bin/python3
#coding=utf-8

from ManifestEditor.BaseChunk import BaseChunk

class ResourceChunk(BaseChunk):
    def __init__(self, all_bytes, offset):
        BaseChunk.__init__(self, all_bytes, offset)
    def print_info(self):
        print("chunk_type", self.chunk_type)
        print("chunk_size", self.chunk_size)