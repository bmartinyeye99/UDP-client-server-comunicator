# UDP-client-server-comunicator

Task Assignment
Design and implement a program using a custom protocol over the User Datagram Protocol (UDP) of the transport layer in the TCP/IP network model. The program should enable communication between two participants on a local Ethernet network, facilitating the transfer of text messages and arbitrary files between computers (nodes).

The program will consist of two parts: a sender and a receiver. The sending node will transmit files to another node in the network. It is assumed that data loss occurs in the network. If the transmitted file is larger than a user-defined maximum fragment size, the sending side will break down the file into smaller parts - fragments - and send them individually. The user should be able to set the maximum fragment size to prevent further fragmentation at the link layer.

If the file is sent as a sequence of fragments, the receiving node will display a message confirming the reception of each fragment along with its sequence number and whether it was received without errors. Upon receiving the entire file at the receiving node, it will display a message indicating successful reception and the absolute path where the received file was saved.

The program must include error checking during communication and the capability to request retransmission of faulty fragments, including both positive and negative acknowledgments. After transmitting the first file, if there is no activity, the communicator will automatically send a packet to maintain the connection every 5-20 seconds until the user terminates the connection. We recommend addressing this through custom-defined signaling messages.

The program must have the following properties (at a minimum):

1. The program must be implemented in C/C++ or Python using libraries for UDP socket operations. It should be compilable and executable in classrooms. The recommended choices are the Python `socket` module, the C/C++ `sys/socket.h` library for Linux/BSD, and `winsock2.h` for Windows. Any other socket-related libraries and functions must be approved by the instructor. The program can also use libraries for working with IP addresses and ports, such as `arpa/inet.h` and `netinet/in.h`.

2. The program must handle data efficiently (e.g., not storing IP addresses as four integers).

3. When sending a file, the user should be able to specify the target IP address and port.

4. The user must have the option to set the maximum fragment size.

5. Both communicating sides must be capable of displaying:
   a. The filename and absolute path on the respective node.
   b. The size and number of fragments.

6. The program should allow simulating transmission errors by sending at least one faulty fragment during file transfer (introducing a deliberate error into the data section of the fragment, causing the receiving side to detect the error).

7. The receiving side must be able to inform the sender about both correct and incorrect fragment deliveries. In the case of incorrect delivery, the receiver should request retransmission of the corrupted data.

8. The program should provide the option to send a 2MB file and save it on the receiving side as the same file. The user only needs to input the directory path where the file should be stored.
