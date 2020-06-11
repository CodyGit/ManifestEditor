#!/usr/bin/python3
#coding=utf-8
#author: cody

from ManifestEditor.AndroidManifest import AndroidManifest
import os

def modify_attr(input_xml, attr_obj, new_attr_obj, output_xml=None):

    if output_xml == None:
        output_xml = input_xml

    android_manifest = AndroidManifest(input_xml)
    tag_chunk = android_manifest.xml_chunk.find_tag_chunk(attr_obj.get("tag"), 
            attr_obj.get("attr_name"), attr_obj.get("attr_value"))

    if type(new_attr_obj) == dict:
        new_attr_obj = [new_attr_obj]
    for attr in new_attr_obj:
        is_string, str_index = tag_chunk.modify(attr.get("key"), attr.get("value"))
        if is_string:
            android_manifest.string_chunk.modify(str_index, attr.get("value"))
    android_manifest.output_bytes(output_xml)

def get_attr_value(input_xml, attr_obj):
    android_manifest = AndroidManifest(input_xml)
    tag_chunk = android_manifest.xml_chunk.find_tag_chunk(attr_obj.get("tag"))
    return tag_chunk.get_attr_value(attr_obj.get("attr_name"))