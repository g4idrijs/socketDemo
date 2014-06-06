#coding: utf8
__author__ = 'watsy'
import struct

from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop

class SocketProxy(object):
    def __init__(self,data):
        if len(data) > 8:
            self._datalength = struct.unpack('I',data[0:4])[0]
            self._command = struct.unpack('I',data[4:8])[0]
            self._datas = data[8:self._datalength + 8]
            self.parse(self._datas)
        else:
            self._datalength = 0

    def parse(self,data):
        pass

    def __len__(self):
        return self._datalength + 8

    @property
    def length(self):
        return self._datalength + 8

    def __unicode__(self):
        return str(struct.unpack('s',self._datas)[0])

    def __str__(self):
        return str(struct.unpack('s',self._datas)[0])

class ChatContent(SocketProxy):
    def parse(self,data):
        self.chatContent = data
        print(self.chatContent)


class Connection(object):
    clients = set()
    def __init__(self, stream, address):
        Connection.clients.add(self)
        self._stream = stream
        self._address = address
        self._datas = b''
        self._stream.set_close_callback(self.on_close)
        self.read_message()
        print("A new user has entered the chat room.", address)

    def read_message(self):
        self._stream.read_until_close(self.broadcast_messages, self.stream_callback)

    def broadcast_messages(self, data):
        pass

    def stream_callback(self, data):
        if len(self._datas) > 0:
            self._datas = '%s%s' % (self._datas, data)
        else:
            self._datas = data

        self.parseTCPProxy()

    def parseTCPProxy(self):
        sProxy = ChatContent(self._datas)
        curLength = len(self._datas)
        length = len(sProxy)
        while (length < curLength):
            if length == curLength:
                self._datas = b''
            else:
                self._datas = self._datas[length,curLength - length]

    def send_message(self, data):
        self._stream.write(data)

    def on_close(self):
        print("A user has left the chat room.", self._address)
        Connection.clients.remove(self)

class ChatServer(TCPServer):
    def handle_stream(self, stream, address):
        print("New connection :", address, stream)
        Connection(stream, address)
        print("connection num is:", len(Connection.clients))

class LoginServer(TCPServer):
    def handle_stream(self, stream, address):
        print("New connection :", address, stream)
        Connection(stream, address)
        print("connection num is:", len(Connection.clients))

if __name__ == '__main__':
    server = ChatServer()
    server.listen(9000)
    loginserv = LoginServer()
    loginserv.listen(9001)
    IOLoop.instance().start()