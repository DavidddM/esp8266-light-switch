import network
from machine import Pin
import usocket as socket
import utime as time

ssid='-'
password='-'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

print(station.ifconfig())

led_pin = Pin(2, Pin.OUT)
led_pin.value(0)

while not station.isconnected():
    pass

led_pin.value(1)

d1_gpio = Pin(5, Pin.OUT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.settimeout(5)
s.bind(('', 80))
s.listen(5)

html = None
last_connection = 0

with open('index.html') as f:
    html = f.read()

while True:
    conn = None
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')
        try:
            command = request.split("\n")[0].split(" ")[1]
        except IndexError:
            pass
        if command:
            if command=='/on' and not d1_gpio.value():
                d1_gpio.value(1)
            elif command=='/off' and d1_gpio.value():
                d1_gpio.value(0)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(html)
        conn.close()
    except OSError:
        if conn:
            conn.close()
    
