# ManifestEditor 修改二进制的AndroidManifest.xml

### 说明

在做apk分发时经常会遇到需要修改`package`、`versionCode`、`versionName`等等**AndroidManifest.xml**中的内容，但是从apk中解压出来的**AndroidManifest.xml**是被处理过的二进制形式，现有的`aapt`或者`AXMLPrinter2.jar`也只能查看并不能修改。原先的思路是用逆向工具`apktool`将apk逆向成project，然后在修改对应的源码版本的xml后再次进行build，但是部分情况下会失败，例如`apktool`版本不对，或者被加壳。

原先做过一个java的版本，只是当时写得比较潦草（结构乱、注释少），碰巧最近又出现了一个Bug。鼓足勇气想在原来的基础上修复，结果一边看一边骂，再加上现在的构建脚本都是用**python**，所以又重新用python翻新了一版修复了Bug。

想了解AndroidManifest.xml的细节，请参考一位大神画的[结构图](https://bbs.pediy.com/thread-194206.htm)

**`ps: 要用python3`**

### 安装

* 方式一：下载源码
    * `git clone https://github.com/CodyGit/ManifestEditor`
    
* 方式二：pip安装
    * `pip install git+https://github.com/CodyGit/ManifestEditor`

### 使用举例 

* 一次性修改同一个`TAG`下的多个属性
* 详细代码可以参考 `test/test.py`


```python
    from ManifestEditor import *
    input_xml = "test/AndroidManifest.xml"
    output_xml = "test/cody-AndroidManifest.xml"
    attr_obj = {
        "tag":"manifest",
    }
    new_attr_obj = [
        {"key": "package", "value": "com.xxx"},
        {"key": "versionCode", "value": 100},
        {"key": "versionName", "value": "2.2.2"}
    ]
    # 不传 `output_xml` 就会把修改后的内容写回 input_xml
    modify_xml_attr(input_xml, attr_obj, new_attr_obj, output_xml)
    
    # 支持直接修改apk，不传 `output_apk` 就会直接把内容修改到原apk中 
    apk_path = "/path/to/apk"
    output_apk = "/path/to/modify-apk"
    modify_apk_attr(apk_path, attr_obj, new_attr_obj, output_apk)
```

* 只修改一个属性

```python
    from ManifestEditor import *
    # 把 android.permission.WRITE_SMS 权限修改成 android.permission.SEND_SMS
    input_xml = "test/AndroidManifest.xml"
    output_xml = "test/cody-AndroidManifest.xml"
    attr_obj = {
        "tag":"uses-permission",
        "attr_name": "name",
        "attr_value": "android.permission.WRITE_SMS"
    }
    new_attr_obj = {"key": "name", "value": "android.permission.SEND_SMS"}
    # 不传 output_xml 就会把修改后的内容写回 input_xml
    modify_xml_attr(input_xml, attr_obj, new_attr_obj, output_xml)
```

如果帮助到您，请不要吝啬您的小星星:star:

### TODO

等有需求再说吧

1. 新增标签和属性
2. 删除标签和属性




