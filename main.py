
import socket
import threading

from Keep_allive import *
import ctypes
import re
import os.path
from os import path



regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

def raise_exception(thread):
    thread_id = get_id(thread)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')

def get_id(thread):

    # returns id of the respective thread
    if hasattr(thread, '_thread_id'):
        return thread._thread_id
    for id, thread in threading._active.items():
        if thread is thread:
            return id


def check_ip(Ip):
    if (re.search(regex, Ip)):
        return True
    else:
        return False



def Client_model():
    print("You are logged in as client")

    ip = input("Enter target ip addres: ")
    while True:
        if check_ip(ip) == True:
            break
        else:
           ip = input("Invalid IP address. Pls re-enter it: ")

    port = int(input("Enter port: "))
    #while not controll_port(ip, port):
    #port = int(input("Invalid port or the port is taken. Pls enter a new port: "))

    frag_size = int(input("enter the size of one fragmet"))
    while frag_size < 30 & frag_size > 1500:
        frag_size = int(input("the entered size is too big or too small"))

    threads = list()
    listener_thread = threading.Thread(target=listen, args=(port + 1, ip, frag_size,os.getcwd()))
    keep_thread = threading.Thread(target=send_keepallive, args=(port, ip))

    threads.append(listener_thread)
    threads.append(keep_thread)

    listener_thread.start()
    keep_thread.start()

    while True:
        action = input("Select action\n\"f\": for files\n"
                       "    \"m\": for message\n"
                       "    \"e\": for damaged message\n"
                       "    \"x\": for exit\n")
        if action == 'f':
            filen = input("Enter name of the file:")
            while True:
                if path.exists(filen) == True:
                    break
                else:
                    filen = input("Enter name of the file: ")

            send_file(filen, ip, port, frag_size)

        elif action == 'm':
            send_message(input("Enter your message: "), ip, port, frag_size)

        elif action == 'e':
            send_damaged_file(input("Enter name of the damaged file: "), ip, port, frag_size)

        elif action == 'x':

            send_exit(port,ip)
            # raise_exception(listener_thread)
            # listener_thread.join()
            # raise_exception(keep_thread)
            # keep_thread.join()
            #listener_thread._stop.set()
            listener_thread.join(timeout=0.00001)
            #keep_thread._stop.set()
            keep_thread.join(timeout=0.00001)

            break

        #print_bytes_sent()

def Server_model():
    print("Logged in as server")
    ip = input("Enter your  IP: ")
    while True:
        if check_ip(ip) == True:
            break
        else:
           ip =  input("Invalid IP address. Pls re-enter it: ")

    port = int(input("Enter number of port: "))
    #while not controll_port(ip, port):
    #port = int(input("Invalid port number. Pls enter a new port: "))

    frag_size = int(input("enter the size of one fragmet received from a socket: "))
    while frag_size < 30 & frag_size > 1500:
        frag_size = int(input("the entered size is too big or too small"))

    print("Add directory where to save incoming files : (format-   C:"+r"\\"+"dir"+r"\\"+ "or press c to save into current directory")
    tmp = input()
    if tmp == 'c':
        save_path = os.getcwd()
    else :
        save_path = tmp

    threads = list()
    listener_thread = threading.Thread(target=listen, args=(port, ip, frag_size,save_path))
    keep_thread = threading.Thread(target=send_keepallive, args=(port + 1, ip))

    threads.append(listener_thread)
    threads.append(keep_thread)

    listener_thread.start()
    keep_thread.start()

    while True:
        action = input("Select action \"x\": for exit\n")
        if action == 'x':
            send_exit(port+1,ip)
            # raise_exception(listener_thread)
            # listener_thread.join()
            # raise_exception(keep_thread)
            # keep_thread.join()

            #listener_thread._stop.set()
            listener_thread.join(timeout=0.00001)
            #keep_thread._stop.set()
            keep_thread.join(timeout=0.00001)
            break

while True:

    print("Chose how u want to proceed:\n"
          "   Type \"s\" if u want to login as server(listener):\n"
          "   Type \"c\" if u want to login as client(sender):\n")

    login_input = input("")
    if login_input == 's':
        Server_model()
    if login_input == 'c':
        Client_model()
    if login_input == 'x':
        break

    # if login_input == 'TS':
    #     port = 5005
    #     ip = "127.0.0.1"
    #     frag_size = 777
    #     #listen(port, ip, frag_size)
    #
    #     threads = list()
    #     listener_thread = threading.Thread(target=listen, args=(port, ip, frag_size, os.getcwd()))
    #     keep_thread = threading.Thread(target=send_keepallive, args=(port + 1, ip))
    #
    #     threads.append(listener_thread)
    #     threads.append(keep_thread)
    #
    #     listener_thread.start()
    #     keep_thread.start()
    #
    # if login_input == 'TC':
    #     port = 5005
    #     ip = "127.0.0.1"
    #     frag_size = 777
    #
    #     threads = list()
    #     listener_thread = threading.Thread(target=listen, args=(port + 1, ip, frag_size,os.getcwd()))
    #     keep_thread = threading.Thread(target=send_keepallive, args=(port, ip))
    #
    #     threads.append(listener_thread)
    #     threads.append(keep_thread)
    #
    #     listener_thread.start()
    #     keep_thread.start()
    #
    #     while True:
    #         action = input("Select action\n\"F\": for files\n"
    #                        "    \"M\": for message\n"
    #                        "    \"E\": for damaged message\n"
    #                        "    \"X\": for exit\n")
    #         if action == 'F':
    #             send_file(input("Enter file name: "), ip, port, frag_size)
    #         elif action == 'M':
    #             send_message(input("Enter message: "), ip, port, frag_size)
    #         elif action == 'E':
    #             send_damaged_file(input("Enter file name: "), ip, port, frag_size)
    #         elif action == 'X':
    #             break
