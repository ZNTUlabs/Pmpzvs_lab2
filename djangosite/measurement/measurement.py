import smbus
import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
bus = smbus.SMBus(1)
address = 0x29
arr = [7,8,18,16,15,13,12,11]

bus.write_byte(address, 0xa0)
bus.write_byte(address, 0x03)
##time.sleep(3)

while True: 
    bus.write_byte(address, 0xac)
    a = bus.read_byte(address)
    bus.write_byte(address, 0xad)
    b = bus.read_byte(address)
    c = a + b*256
    print(c)
   ##time.sleep(0.1) 
  
    if c > 300:
        for i in arr:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, True)
            ##time.sleep(0.5)
    elif c < 300:
        for i in [7,8,18,16]:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, False)
            ##time.sleep(1)
        
    with open('measurement.log', 'a+') as file:
        file.write(str(c) + '\n')

    time.sleep(0.5) 