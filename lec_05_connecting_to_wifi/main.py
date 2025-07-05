import socket
import time
import network

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('SharyAr','shinka11145')

while wifi.isconnected()==False:
    print('waiting for connection...')
    time.sleep(1)
wifiInfo = wifi.ifconfig()
print(wifiInfo)
serverip = wifiInfo[0]
serverport = 2222
buffersize = 1024
udpserver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
udpserver.bind((serverip,serverport))
msg,addr = udpserver.recvfrom(buffersize)
msgDecode = msg.decode('utf-8')
print(msgDecode)
