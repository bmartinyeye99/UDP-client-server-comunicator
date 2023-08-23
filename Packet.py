import sys
import base64


def get_chechsum(payload):

    return int.from_bytes(payload, "big") % 255

def create_header(mtype, order):

    b_type = bytes(hex(mtype).zfill(1), 'utf-8')    # typ packetu je od 0-5 teda v hexa bude max max dlzku 1
    b_order = bytes(hex(order).zfill(8),'utf-8')  # ked predpokladam ze pocet paketov bude < 1 mil. tak hexa hodnota ma 5 cislic

    #b_order = bytes(hex(order).zfill(5), 'utf-8')   # ked predpokladam ze pocet paketov bude < 1 mil. tak hexa hodnota ma 5 cislic
    return b_type + b_order

def create_package(type, fragment, order):
    header = create_header(type, order)
    b_csum = bytes(hex(get_chechsum(header + fragment)).zfill(4), 'utf-8')
    pack = bytes(header + fragment + b_csum)

    return pack

# def create_currupted_package(type, fragment, order):
#     header = create_header(type, order)
#     b_csum = bytes(hex(get_chechsum(header + fragment)).zfill(4), 'utf-8')
#     pack = bytes(header + fragment + b'1' + b_csum)
#
#     return pack

def check_chechsum(payload, checksum):

    hash = int.from_bytes(payload, "big") % 255
    if hash == int(((checksum.decode("utf-8")).lstrip("0")).lstrip("x"), 16):
        return True
    return False

def decod_packet(message):
    type = int(((message[:3].decode("utf-8")).lstrip("0")).lstrip("x"), 16)
    checksum = int.from_bytes(message[-4:], byteorder='little')
    order = int(((message[3:11].decode("utf-8")).lstrip("0")).lstrip("x"), 16)
    data = message[11:-4]
    # order = int(((message[3:8].decode("utf-8")).lstrip("0")).lstrip("x"), 16)
    # data = message[8:-4]

    return type, order, data

def get_corrupted_checksum(payload):
    return int.from_bytes(payload,"big") % 255

def create_corrupted_package(type, fragment, order):
    header = create_header(type, order)
    b_csum = bytes(hex(get_corrupted_checksum(header + fragment)).zfill(4), 'utf-8')
    pack = bytes(header + (fragment+b'1') + b_csum )

    return pack