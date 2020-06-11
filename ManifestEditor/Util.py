#!/usr/bin/python3
#coding=utf-8
#author: cody

def create_reader(byte_arr, offset):
    f = offset
    b_arr = byte_arr
    def read(count):
        nonlocal f
        nonlocal b_arr
        b = b_arr[f:f + count]
        f = f + count
        return b
    return read

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='little',signed=True)

def int_to_bytes(i, l=4):
    return i.to_bytes(length=l, byteorder='little',signed=True)

def float_to_bytes(f):
    import ctypes
    i = ctypes.c_uint.from_buffer(ctypes.c_float(f)).value
    return self.int_to_bytes(i)

def bytes_to_hex(b, byteorder='little'):
    new_bytes = b
    if byteorder == "little":
        new_bytes = bytearray(b)
        new_bytes.reverse()
        return "0x" + new_bytes.hex()
    else:
        return "0x" + b.hex()