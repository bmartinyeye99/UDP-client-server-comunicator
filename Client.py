import socket
import time
import threading
import sys

from Packet import *
#from Keep_allive import *
#from Main import set_bytesSent
import os



ConnectionTryTimeot = 10
ConnectinStatus = True
packetHist = list()
packToSend = list()

byteSent = 0
packetSent = 0

def print_bytes_sent():
    global  byteSent
    global packetSent

    print(byteSent, "bytes sent in", packetSent, "packet")

def send_data(package, IP, port):
    global bytesSent

    global byteSent
    global packetSent

    type, order, data_d = decod_packet(package)

    #if order % 2 == 0:
    #    package = (create_currupted_package(type,data_d,order), (IP, port))
    byteSent += (sys.getsizeof(data_d))

    packetSent += 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(package, (IP, port))

def send_exit(port, IP):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pack = create_package(6, "hello".encode("utf-8"), 0)
    sock.sendto(pack, (IP, port))

def send_file(fileName,IP, port, chunk_size):

    global packetHist
    packetHist.clear()
    packToSend.clear()
    chunk_size -= 29    #header size + byte conversion

    print("file saved to ", os.getcwd() + "\\" + fileName)
    with open(fileName, "rb") as f_message:
        counter = 0
        while 1:
            fileData = f_message.read(chunk_size)
            #print(chunk_size," byte from file was riden\n")
            pack = create_package(3, fileData, counter)
            packetHist.append(pack)
            if fileData == "".encode("utf-8"):
                break
            packToSend.append(counter)
            counter += 1


        send_data(create_package(2, fileName.encode("utf-8"), counter), IP, port)
        while len(packToSend) > 0:
            i = 0
            for i in packToSend:
                time.sleep(0.00001)
                #sock.sendto(packetHist[i], (IP, port))
                print("Sender : packet n.", i, "send")
                #if i % 2 == 0:
                     #print("Sender : Corrupted file sent - packet n. ", i, "sent")
                 #   send_data(create_corrupted_package(3, packetHist[i][8:-4], i), IP, port)
                #else :
                print("Sender : packet n.", i, "send")
                send_data(packetHist[i], IP, port)

            time.sleep(0.1)


        send_data(create_package(4, b'', i), IP, port)

        f_message.close()

def resend_packet(order, IP, port, chunk_size):
    print("Sender : resending packet:", order)

    send_data(packetHist[order], IP, port)

def send_message(message,IP, port, chunk_size):

    chunk_size -= 29
    i = 0
    while 1:
        if i > len(message):
            break
        send_data(create_package(1, message[i:i+chunk_size].encode("utf-8"), 0), IP, port)
        i += chunk_size
    print_bytes_sent()



def send_damaged_file(fileName,IP, port, chunk_size):

    global packetHist
    packetHist.clear()
    packToSend.clear()
    chunk_size -= 29
    damage = True

    with open(fileName, "rb") as f_message:
        counter = 0
        while 1:
            fileData = f_message.read(chunk_size)

            pack = create_package(3, fileData, counter)
            packetHist.append(pack)
            if fileData == "".encode("utf-8"):
                break
            packToSend.append(counter)
            counter += 1



        send_data(create_package(2, fileName.encode("utf-8"), counter), IP, port)       # poslem 1. packet chybneho suboru

        while len(packToSend) > 0:
            i = 0
            for i in packToSend:
                time.sleep(0.00001)
                if i % 5 == 0 :
                    print("Sender : Corrupted file sent - packet n. ",i,"sent")

                    send_data(create_corrupted_package(3, packetHist[i][8:-4], i), IP, port)
                    damage = False
                else:
                    send_data(packetHist[i], IP, port)
                    print("Sender : packet n.", i, "send")
            time.sleep(0.1)

        send_data(create_package(4, b'', i), IP, port)

        f_message.close()


