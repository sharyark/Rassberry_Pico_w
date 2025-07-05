import network
import socket
import time

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('SharyAr', 'shinka11145')

while not wifi.isconnected():
    print('Connecting to WiFi...')
    time.sleep(1)

print('Connected:', wifi.ifconfig())

# Function to perform HTTP GET request
def http_get(url, host):
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    request = f"GET {url} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    s.send(request.encode())

    response = b""
    while True:
        data = s.recv(512)
        if not data:
            break
        response += data
    s.close()
    return response.decode()

# Example: Get data from example.com (HTTP only)
host = "example.com"
url = "/"
html = http_get(url, host)
print("Website content:\n")
print(html)
