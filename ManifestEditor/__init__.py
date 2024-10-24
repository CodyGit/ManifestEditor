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

def modify_apk_attr(input_apk, attr_obj, new_attr_obj, output_apk=None):
    tmp_xml = _get_androidmanifest(input_apk)
    modify_xml_attr(tmp_xml, attr_obj, new_attr_obj)
    tmp_apk = tempfile.mktemp('.apk')
    # zipfile不支持直接更新里面的某个文件
    # 现在的方案是把A中的所有文件重新写入一个新的zip中，过滤掉需要修改的部分
    with zipfile.ZipFile(input_apk, "r", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_in:
        with zipfile.ZipFile(tmp_apk, 'a', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zip_out:
            zip_out.comment = zip_in.comment 
            for item in zip_in.infolist():
                if item.filename == "AndroidManifest.xml":
                    zip_out.write(tmp_xml, item.filename)
                    continue
                zip_out.writestr(item, zip_in.read(item.filename))
    zip_in.close()
    zip_out.close()
    if not output_apk:
        output_apk = input_apk
    shutil.move(tmp_apk, output_apk)

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
