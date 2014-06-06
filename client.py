#! /usr/bin/env python  
#coding=utf-8  
  
import socket
import struct
  
HOST = '127.0.0.1'    # The remote host  
PORT = 9001           # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.connect((HOST, PORT))

values = (11,4,'hello world'.encode())
packer = struct.Struct('I I 11s')
packed_data = packer.pack(*values)

# for i in range(1,10):
#     s.sendall(packed_data)
s.sendall(packed_data)

s.close() 