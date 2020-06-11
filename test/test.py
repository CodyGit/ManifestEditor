
from ManifestEditor import *

def test():
    input_xml = "test/AndroidManifest.xml"
    output_xml = "test/cody-AndroidManifest.xml"
    old_attr_obj = {
        "tag":"manifest",
    }
    new_attr_obj = [
        {"key": "package", "value": "com.xxx"},
        {"key": "versionCode", "value": 100},
        {"key": "versionName", "value": "2.2.2"}
    ]
    modify_attr(input_xml, old_attr_obj, new_attr_obj, output_xml)
    print(get_attr_value(input_xml, {"tag":"manifest","attr_name":"package"}))

if __name__ == "__main__":
    test()