
from ManifestEditor import *

base = os.path.dirname(os.path.abspath(__file__))
def test():
    input_xml = os.path.join(base, "AndroidManifest.xml")
    output_xml = os.path.join(base, "cody-AndroidManifest.xml")
    old_attr_obj = {
        "tag":"manifest",
    }
    new_attr_obj = [
        {"key": "package", "value": "com.xxx1"},
        {"key": "versionCode", "value": 100},
        {"key": "versionName", "value": "2.2.2"}
    ]
    modify_xml_attr(input_xml, old_attr_obj, new_attr_obj, output_xml)
    print(get_xml_attr(input_xml, {"tag":"manifest","attr_name":"package"}))

def test_apk():
    apk_path = os.path.join(base, "cody.apk")
    old_attr_obj = {
        "tag":"manifest",
    }
    new_attr_obj = [
        {"key": "package", "value": "com.xxx1"},
        {"key": "versionCode", "value": 100},
        {"key": "versionName", "value": "2.2.2"}
    ]
    modify_apk_attr(apk_path, old_attr_obj, new_attr_obj)
    print(get_apk_attr(apk_path, {"tag":"manifest","attr_name":"package"}))

if __name__ == "__main__":
    test()
    test_apk()