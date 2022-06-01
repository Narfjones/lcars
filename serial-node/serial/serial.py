from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL 
import serial
import logging
from time import sleep

chosenPort = str()
ser = None
running = None
speed = None
rpm = None

def init():    
    global chosenPort
    global ser
    global chosenPort
    global running

    running = True
    logging.debug('Program Initiated')

def connectSerial():
    global ser
    try:
        ser = serial.Serial(
        port = chosenPort,\
        baudrate=115200,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
        sleep(.001) # Short sleep is necessary apparently
        print("connected to: " + chosenPort)
        logging.debug('Serial Port connected')
        print(speed, rpm)
    except: # If an exception is thrown we assume it is already connected. Needs to be more specific.
        logging.debug('Serial Port was unable to connect')
        pass

def serial_conversion(line, valIndex):
    info_lst = line.split("|")
    try:
        infoStr = str(info_lst[valIndex])
    except IndexError:     
        infoStr = 'null'
    return infoStr

def getValues():

    while True: 
        try:
            if (ser.in_waiting > 0): # Checks if there is data in the serial buffer. Always true if connected

                    # Create variables to store value to check against for change
                    previousVals= []

                    #timeStart = float( time.perf_counter())
                    # create string, convert serial input data to a string a store it
                    line =  str(ser.readline())
                    ser.reset_input_buffer()
                    
                    varStrs = []
                    vars = 2
                    for i in len(vars):
                        varStrs.append(''.join(x for x in serial_conversion(line, i) if x.isdigit()))

                    else: # Skip if no sliders or no process assignments
                        pass

                    # Check new value against previous value and send new volume if it has changed

                    for i in len(vars):
                        if varStrs[i] != previousVals[i]:
                            previousVals[i] = varStrs[i]
                                # Do something here to get the values to the SpeedoTach Vue component
                        else:
                            pass

                    if running == False:
                        break
                    else:
                        pass

        except serial.serialutil.SerialException:
            if running == False:
                break
            else:
                pass
            print('SerialException: Cannot check in_waiting')