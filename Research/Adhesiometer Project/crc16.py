# uncompyle6 version 3.2.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 2.7.15rc1 (default, Apr 15 2018, 21:51:34) 
# [GCC 7.3.0]
# Embedded file name: C:\Users\Dart\Documents\WorkSpace\adheziometer\pc_software\crc16.py
# Compiled at: 2018-07-23 19:54:02
# Size of source mod 2**32: 951 bytes

try:
    import port_tests
except Exception as e:
    print('COM in not working')
    exit()

    
POLYNOMIAL = 4129
PRESET = 65535

def _initial(c):
    crc = 0
    c = c << 8
    for j in range(8):
        if (crc ^ c) & 32768:
            crc = crc << 1 ^ POLYNOMIAL
        else:
            crc = crc << 1
        c = c << 1

    return crc


_tab = [_initial(i) for i in range(256)]

def _update_crc(crc, c):
    cc = 255 & c
    tmp = crc >> 8 ^ cc
    crc = crc << 8 ^ _tab[tmp & 255]
    crc = crc & 65535
    return crc


def crc(str1):
    crc = PRESET
    for c in str1:
        crc = _update_crc(crc, ord(chr(c)))

    return crc


def crcb(*i):
    crc = PRESET
    for c in i:
        crc = _update_crc(crc, c)

    return crc


def calc(data):
    sp = [i for i in data]
    ssp = ('').join(sp)
    return crc(ssp)


def _selfTest():
    packet = bytearray([0, 1, 0, 2, 0, 3])
    if calc(packet) == 64066:
        print('test ok')


print('Program running...')
# okay decompiling /home/workingcloud/asd/crc16.cpython-35.pyc
