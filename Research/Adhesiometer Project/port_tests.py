import serial.tools.list_ports
ports = serial.tools.list_ports.comports()


if len(ports) == 0:
    print('COM ports are not avaliable!')
else: 
    for port, desc, hwind in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwind))

input('Press Enter To continue...')