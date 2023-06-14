import os, pty, serial
import time

master, slave = pty.openpty()
s_name = os.ttyname(slave)

ser = serial.Serial(s_name)

# To Write to the devi

# To read from the dev

while True:
    s_name = os.ttyname(slave)

    ser = serial.Serial(s_name)
    print(s_name)
    time.sleep(0.2)