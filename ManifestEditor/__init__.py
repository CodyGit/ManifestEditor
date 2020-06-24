#!/usr/bin/python3
#coding=utf-8
#author: cody

from ManifestEditor.AndroidManifest import AndroidManifest
import os
import zipfile
import tempfile
import shutil

# private
def _get_androidmanifest(input_apk):
    if not os.path.exists(input_apk):
        raise Exception("%s not exists"%(input_apk))

    tmp_xml = tempfile.mktemp('.xml')
    with open(tmp_xml, "wb") as output_stream:
        zip_stream = zipfile.ZipFile(input_apk, "r")
        xml_data = zip_stream.read("AndroidManifest.xml")
        output_stream.write(xml_data)
        zip_stream.close()
    return tmp_xml

def modify_apk_attr(input_apk, attr_obj, new_attr_obj):
    tmp_xml = _get_androidmanifest(input_apk)
    modify_xml_attr(tmp_xml, attr_obj, new_attr_obj)

    zip_stream = zipfile.ZipFile(input_apk, "w", zipfile.ZIP_DEFLATED)
    zip_stream.write(tmp_xml, "AndroidManifest.xml")
    zip_stream.close()

def get_apk_attr(input_apk, attr_obj):
    tmp_xml = _get_androidmanifest(input_apk)
    return get_xml_attr(tmp_xml, attr_obj)


def modify_xml_attr(input_xml, attr_obj, new_attr_obj, output_xml=None):
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

def get_xml_attr(input_xml, attr_obj):
    android_manifest = AndroidManifest(input_xml)
    tag_chunk = android_manifest.xml_chunk.find_tag_chunk(attr_obj.get("tag"))
    return tag_chunk.get_attr_value(attr_obj.get("attr_name"))