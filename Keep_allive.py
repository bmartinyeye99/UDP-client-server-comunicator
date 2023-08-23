import time
import socket

from Client import *
from Packet import *
import os
import timeit


ConnectionTryTimeot = 6
ConnectinStatus = True

acks = 0
nacks = 0
total_size_of_msgs = 0
total_size_of_filedata = 0

def send_keepallive(port, IP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pack = create_package(0, "hello".encode("utf-8"), 0)
    global ConnectionTryTimeot
    global ConnectinStatus

    while ConnectionTryTimeot:
        #print("sent hello")
        sock.sendto(pack, (IP, port))
        time.sleep(10)
        ConnectionTryTimeot -= 1

    ConnectinStatus = False
    print("Connection try failed (timeout). Connection lost.")

def print_ACK():
    global acks
    global nacks

    print("Number of ACKs (correctly received packets): ", acks, "Number of NACK (damaged packets): ", nacks)

def listen(port, ip, frag_size,save_path):
    global ConnectionTryTimeot
    global ConnectinStatus
    global acks
    global nacks

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))

    buffer = list()
    buffer.clear()
    while True:
        data, addr = sock.recvfrom(frag_size)
        type, order, data_d = decod_packet(data)

        if type == 6:
            print("Other side quited the connection, please sign out. Press X \n")
            return

        elif type == 0:
            ConnectionTryTimeot = 10

        # výpis správy
        elif type == 1:
            print(data_d.decode("utf-8"))


        # 1. packet of a file warning that file fragments are incoming + it holds the filename
        elif type == 2:

            fileName = '2' + data_d.decode("utf-8")

            completeName = os.path.join(save_path, fileName)

            file = open(completeName, "wb+")
            pack_len = order
            packet_counter = 0

            buffer = [b'' * frag_size] * pack_len
            start = timeit.default_timer()


        # rest of the file fragments
        elif type == 3:
            print("Reciever : packet n.", order, "size of: ", sys.getsizeof(data), "arrived")
            if check_chechsum(data[:-4], data[-4:]) == True:
                buffer[order] = data_d
                packet_counter += 1
                print("Reciever : checksum ok")


                global total_size_of_filedata
                global total_size_of_msgs
                total_size_of_msgs += sys.getsizeof(data)
                total_size_of_filedata += sys.getsizeof(data_d)
                acks += 1

                sock.sendto(create_package(5, "ok".encode("utf-8"), order), (ip, port + 1))

            elif check_chechsum(data[:-4], data[-4:]) == False:
                print("Reciever : checksum error. Requested for resend")
                nacks += 1
                sock.sendto(create_package(5, "err".encode("utf-8"), order), (ip, port + 1))


        # las packet of the file
        elif type == 4:

            if packet_counter == pack_len:
                print("\n Reciever : all packets have arrived")
            print("Reciever : file saved to ", completeName)
            for i in range(pack_len):
                file.write(buffer[i])

            print_ACK()
            print("Total number of packeges (correct and damaged) : ", acks + nacks)
            file.close()
            end = timeit.default_timer()
            print("Time taken for the file transfer: ",end-start)
            print("Total amount of data recieved (correct packeges only) in B:",total_size_of_msgs ," kB: ",total_size_of_msgs/100  ," MB: " ,total_size_of_msgs/1000)
            print("Total amount of file-data recieved (correct packeges only) in B: ",total_size_of_msgs ," kB: ",total_size_of_filedata/100  , " MB: ", total_size_of_filedata/1000)

            total_size_of_msgs = 0
            total_size_of_filedata = 0
            buffer.clear()
            acks = 0
            nacks = 0
            # for the reciever
        elif type == 5:
            if data_d.decode("utf-8") == "ok":
                print("\n Reciever : packet:", order, "arrived ok")
                packToSend.remove(order)
            else:
                print("\n Reciever : resend request for packet:", order, "recived")
                resend_packet(order, ip, port - 1, frag_size)




