import socket
serveraddre = ('192.168.1.4',2222)
buffersize = 1024
udpclient = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    cmd = input('what is your command')
    cmdEncoded = cmd.encode('utf-8')
    udpclient.sendto(cmdEncoded,serveraddre)