#!/usr/bin/python3
#coding=utf-8
#author: cody

"""
 * Container for a dynamically typed data value.  Primarily used with
 * {@link android.content.res.Resources} for holding resource values.
 参考android 源码实现
"""
class TypedValue:
    TYPE_NULL = 0
    TYPE_REFERENCE = 1
    TYPE_ATTRIBUTE = 2
    TYPE_STRING = 3
    TYPE_FLOAT = 4
    TYPE_DIMENSION = 5
    TYPE_FRACTION = 6
    TYPE_FIRST_INT = 16
    TYPE_INT_DEC = 16
    TYPE_INT_HEX = 17
    TYPE_INT_BOOLEAN = 18
    TYPE_FIRST_COLOR_INT = 28
    TYPE_INT_COLOR_ARGB8 = 28
    TYPE_INT_COLOR_RGB8 = 29
    TYPE_INT_COLOR_ARGB4 = 30
    TYPE_INT_COLOR_RGB4 = 31
    TYPE_LAST_COLOR_INT = 31
    TYPE_LAST_INT = 31

    COMPLEX_UNIT_SHIFT = 0
    COMPLEX_UNIT_MASK = 15
    COMPLEX_UNIT_PX = 0
    COMPLEX_UNIT_DIP = 1
    COMPLEX_UNIT_SP = 2
    COMPLEX_UNIT_PT = 3
    COMPLEX_UNIT_IN = 4
    COMPLEX_UNIT_MM = 5
    COMPLEX_UNIT_FRACTION = 0
    COMPLEX_UNIT_FRACTION_PARENT = 1
    COMPLEX_RADIX_SHIFT = 4
    COMPLEX_RADIX_MASK = 3
    COMPLEX_RADIX_23p0 = 0
    COMPLEX_RADIX_16p7 = 1
    COMPLEX_RADIX_8p15 = 2
    COMPLEX_RADIX_0p23 = 3
    COMPLEX_MANTISSA_SHIFT = 8
    COMPLEX_MANTISSA_MASK = 16777215 # 0xffffff
    DATA_NULL_UNDEFINED = 0
    DATA_NULL_EMPTY = 1
    DENSITY_DEFAULT = 0
    DENSITY_NONE = 65535 # 0xffff

    DIMENSION_UNIT_STRS = [
        "px", "dip", "sp", "pt", "in", "mm"
    ]
    FRACTION_UNIT_STRS = [
        "%", "%p"
    ]
    MANTISSA_MULT = 1.0 / (1<<COMPLEX_MANTISSA_SHIFT)
    RADIX_MULTS = [
        1.0 * MANTISSA_MULT, 1.0 /(1<<7)*MANTISSA_MULT,
        1.0/(1<<15)*MANTISSA_MULT, 1.0/(1<<23)*MANTISSA_MULT
    ]
    STRING_ARR = []
    @staticmethod
    def setStringArr(string_arr):
        TypedValue.STRING_ARR = string_arr

    @staticmethod
    def complexToFloat(complex):
        return (complex & (TypedValue.COMPLEX_MANTISSA_MASK << TypedValue.COMPLEX_MANTISSA_SHIFT)) * TypedValue.RADIX_MULTS[
            (complex>>TypedValue.COMPLEX_RADIX_SHIFT) & TypedValue.COMPLEX_RADIX_MASK
            ]

    @staticmethod
    def coerceToString(type_int, data_int):
        if type_int == TypedValue.TYPE_NULL:
            return None
        elif type_int == TypedValue.TYPE_REFERENCE:
            return "@%s%s"%(TypedValue.getPackage(data_int), Integer.toHexString(data_int))
        elif type_int == TypedValue.TYPE_ATTRIBUTE:
            return "?%s%s"%(TypedValue.getPackage(data_int), Integer.toHexString(data_int))
        elif type_int == TypedValue.TYPE_FLOAT:
            return Float.toString(Float.intBitsToFloat(data_int))
        elif type_int == TypedValue.TYPE_DIMENSION:
            return Float.toString(TypedValue.complexToFloat(data_int)) + TypedValue.DIMENSION_UNIT_STRS[
                (data_int>>TypedValue.COMPLEX_UNIT_SHIFT) & TypedValue.COMPLEX_UNIT_MASK]
        elif type_int == TypedValue.TYPE_FRACTION:
            return Float.toString(TypedValue.complexToFloat(data_int)*100) + TypedValue.FRACTION_UNIT_STRS[
                (data_int>>TypedValue.COMPLEX_UNIT_SHIFT)& TypedValue.COMPLEX_UNIT_MASK]; 
        elif type_int == TypedValue.TYPE_INT_HEX:
            return Integer.toHexString(data_int)
        elif type_int == TypedValue.TYPE_INT_BOOLEAN:
            return "true" if data_int != 0 else "false"
        elif type_int == TypedValue.TYPE_STRING:
            return TypedValue.STRING_ARR[data_int]
        elif (type_int >= TypedValue.TYPE_FIRST_COLOR_INT 
            and type_int <= TypedValue.TYPE_LAST_COLOR_INT):
            return "#" + Integer.toHexString(data_int)
        elif (type_int >= TypedValue.TYPE_FIRST_INT 
            and type_int <= TypedValue.TYPE_LAST_INT):
            return Integer.toString(data_int)
        return None

    @staticmethod
    def convertToString(v_int):
        if v_int == -1 or v_int >= len(TypedValue.STRING_ARR):
            return ""
        else:
            return TypedValue.STRING_ARR[v_int]

    """
    参考网上的实现
    https://github.com/fourbrother/AXMLEditor/blob/master/src/cn/wjdiankong/main/AttributeType.java
    """
    @staticmethod 
    def getPackage(data_int):
        if (data_int >> 24 == 1 ):
            return "android:"
        return ""
    
from ctypes import *
class Float:
    # @staticmethod
    # def intToBin32(i):
    #     return (bin(((1 << 32) - 1) & i)[2:]).zfill(32)
    # @staticmethod
    # def intBitsToFloat(v_int):
    #     bits = Float.intToBin32(v_int)
    
    @staticmethod
    def intBitsToFloat(v_int):
        # i = int(s, 16)                 
        cp = pointer(c_int(v_int))          
        fp = cast(cp, POINTER(c_float)) 
        return fp.contents.value
    @staticmethod
    def toString(v):
        return str(v)

class Integer:
    @staticmethod
    def toString(v):
        return str(v)
    # TODO
    # 这里和java的实现有些不一致，java的实现不会补全8位并且没有 0x
    # 等调试ResourceChunk的时候再调整
    def toHexString(v_int, len = 8):
        if len:
            tmp = hex(v_int)
            return "0x%s"%(tmp[2:].zfill(len))
        else:
            return hex(v_int)