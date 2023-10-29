import network
import socket
from time import sleep
import machine
from machine import Pin, PWM

# Yes, these could be in another file. But on the Pico! So no more secure. :)
ssid = 'wifi name'
password = 'password'

#set up pins
eye = PWM(Pin(0))
lid = PWM(Pin(1))
btn1 = Pin(20, Pin.IN, Pin.PULL_DOWN)
btn2 = Pin(21, Pin.IN, Pin.PULL_DOWN)
btn3 = Pin(22, Pin.IN, Pin.PULL_DOWN)

eye.freq(50)
lid.freq(50)

left = 2000
right = 7500
middle = 5000
opn = 6000
clsd = 4000

#servo functions
def setEyeCycle(position):
    eye.duty_u16(position)
    sleep(0.01)
    
def setLidCycle(position):
    lid.duty_u16(position)
    sleep(0.01)
    
def look(direction):
    eye.duty_u16(direction)
    sleep(0.01)
    
def eye_lid(opnclsd):
    lid.duty_u16(opnclsd)
    sleep(0.01)
    

#wifi stuff   
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Eye Control</title>
            </head>
            <center><b>
            <form action="./open">
            <input type="submit" value="Open" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./mid">
            <input type="submit" value="Middle" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./closed">
            <input type="submit" value="Closed" style="height:120px; width:120px" />
            </form>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/open?':
            eye_lid(opn)
        elif request =='/left?':
            look(left)
        elif request =='/mid?':
            look(middle)
        elif request =='/right?':
            look(right)
        elif request =='/closed?':
            eye_lid(clsd)
        html = webpage()
        client.send(html)
        client.close()
#main
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

    