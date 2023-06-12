import os, pty, serial
import time

master, slave = pty.openpty()
s_name = os.ttyname(slave)

ser = serial.Serial(s_name)

# To Write to the devi

# To read from the dev

while True:
    print(f'write into {s_name} your text')
    my_text = 'Your text'.encode()
    ser.write(my_text)
    time.sleep(1)