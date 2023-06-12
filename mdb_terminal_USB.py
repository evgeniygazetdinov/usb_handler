import serial
import time
import serial.tools.list_ports as ports


def find_availiable_ports():
    com_ports = list(ports.comports())

    return [i.device for i in com_ports]

Count = 0
Response = 0
Vend = False
DoOnce = True
Port = "/dev/ttys009"
Reset = bytearray([0x10])  # Reset
Setap = bytearray([0x11, 0x00, 0x03, 0x00, 0x00, 0x00])  # Setap
Setap2 = bytearray([0x11, 0x01, 0x03, 0xE8, 0x00, 0x00])  # Setap2 Max/Min prices
RequestID = bytearray([0x17, 0x00, 0x4D, 0x45, 0x49, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x4E, 0x47, 0x43, 0x20, 0x4D, 0x44, 0x42, 0x20, 0x30, 0x30, 0x30, 0x31, 0x01, 0x27])  # Expansion2
Expansion = bytearray([0x17, 0x04, 0x00, 0x00, 0x00, 0x20])  # Expansion
Enable = bytearray([0x14, 0x01])  # Enable
VendRequest = bytearray([0x13, 0x00, 0x00, 0x01, 0x00, 0x00])  # VendRequest
VendRequest2 = bytearray([0x13, 0x00, 0x03, 0xE8, 0x00, 0x00])  # VendRequest
VendCancel = bytearray([0x13, 0x01])  # vend_cancel
VendSuccess = bytearray([0x13, 0x02, 0x00, 0x00])  # vend_success
VendFailure = bytearray([0x13, 0x03])  # vend_failure
SessionComplete = bytearray([0x13, 0x04])  # session_complete
Disable = bytearray([0x14, 0x00])  # DISABLE
Limit_request = bytearray([0x15, 0x01])  # Revalue limit request
SelectionDenied = bytearray([0x13, 0x07])
Poll = bytearray([0x12])
ACK = bytearray([0x00])
NAK = bytearray([0xff])
print(find_availiable_ports())
port = serial.Serial(Port, 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)  # "/dev/ttyUSB0"  "COM3"
Initialization = True

 # returns 'COMx'

def click_price(money_price):
    global Vend

    Vend = True
    money = int(money_price)

    if money < 256:
        VendRequest[3] = money_price
        processing_byte(VendRequest, 250)
    else:
        count = 1
        an_back = 2
        bytes_array = money_price.to_bytes(2, 'little')

        for i in range(len(bytes_array)):
            count += 1
            an_back -= 1
            VendRequest2[count] = bytes_array[an_back]
        
        processing_byte(VendRequest2, 250)

def data_received_handler(indata):
    global Response, Count

    S = list(indata.encode())
    for i in range(len(S)):
        if S[i] > 0:
            print(S[i])

        Response = S[i]
        if S[i] == 3:
            processing_byte(VendRequest, 250)
        if S[i] == 5:
            print("APPROVED")
        if S[i] == 6:
            Count += 1
            if Count == 2:
                processing_byte(ACK, 250)
                processing_byte(VendSuccess, 250)
                processing_byte(SessionComplete, 250)
                print("DENIED")
                Count = 0
        if S[i] == 4:
            pass
        if S[i] == 7:
            processing_byte(ACK, 250)
            processing_byte(Disable, 250)
            processing_byte(Enable, 250)
            processing_byte(SelectionDenied, 250)

def data_received():
    indata = port.read(port.inWaiting())
    data_received_handler(indata.decode())

def terminal_card():
    while True:
        global Initialization

        if Initialization:
            initialization_terminal()
            Initialization = False
        else:
            processing_byte(Poll, 200)

def initialization_terminal():
    processing_byte(Reset, 250)
    processing_byte(Setap, 250)
    processing_byte(Setap2, 250)
    processing_byte(ACK, 250)
    processing_byte(RequestID, 250)
    processing_byte(ACK, 250)
    processing_byte(Expansion, 250)
    processing_byte(Enable, 250)
    processing_byte(VendRequest2, 250)
    print("VendRequest")

def processing_byte(commands, sleep):
    checksum = cal_checksum(commands, len(commands))
    summ = bytearray([checksum])

    time.sleep(sleep / 1000)
    port.parity = serial.PARITY_MARK

    port.write(commands)
    port.parity = serial.PARITY_SPACE

    port.write(summ)

def cal_checksum(packet_data, packet_length):
    check_sum_byte = 0x00
    for i in range(packet_length):
        check_sum_byte += packet_data[i]
    return check_sum_byte & 0xFF



def main():
    """ точка входа"""
    # port.open() s
    port.rts = True
    port.timeout = 0.005

    while port.inWaiting() > 0:
        data_received()
    port.close()
    
if __name__ == '__main__':
    main()



