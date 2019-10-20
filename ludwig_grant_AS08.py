# File Name: ludwig_grant_AS08.py
# File Path: /home/ludwigg/Python/PyRpi_AS8/ludwig_grant_AS08.py
# Run Command: sudo python3 /home/ludwigg/Python/PyRpi_AS8/ludwig_grant_AS08.py

# Grant Ludwig
# 10/23/2019
# AS.08
# HCreate a target shooting game

from graphics import *
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import RPi.GPIO as GPIO # Raspberry Pi GPIO library

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
target = Circle(Point(250, 250), 10)

win = GraphWin("Target Practice", SCREEN_WIDTH, SCREEN_HEIGHT, autoflush=False)

def getXPosition():
    global chan
    return -round(chan.voltage/3.3 * SCREEN_WIDTH)

def getYPosition():
    global chan2
    return -round(chan2.voltage/3.3 * SCREEN_HEIGHT)

def setupTarget():
    target.setFill("Red")
    target.draw(win)

def shoot():
    return

def main():
    win.setBackground("Grey")

    setupTarget()

    while(true):
        target.undraw()
        target = Circle(Point(getXPosition(), getYPosition()), 10)
        target.draw()
        update(30)
    
    win.close()

# Setup GPIO
GPIO.setwarnings(False) # Ignore warnings
GPIO.setmode(GPIO.BCM) # Use BCM Pin numbering
GPIO.setup(26, GPIO.IN)

GPIO.add_event_detect(26, GPIO.FALLING, callback=shoot, bouncetime=300)
	
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P0)
chan2 = AnalogIn(mcp, MCP.P1)
zeroY = round(chan.voltage/3.3, 1)
zeroX = round(chan2.voltage/3.3, 1)
# print("zeroY: ", zeroY)
# print("zeroX: ", zeroX)

# print("x: ", (round(chan2.voltage/3.3, 1) - zeroX))
# print("y: ", (round(chan.voltage/3.3, 1) - zeroY))
try:
    print("Before Main")
    main()
    print("After main")

except KeyboardInterrupt: 
    # This code runs on a Keyboard Interrupt <CNTRL>+C
    print('\n\n' + 'Program exited on a Keyboard Interrupt' + '\n') 

except: 
    # This code runs on any error
    print('\n' + 'Errors occurred causing your program to exit' + '\n')

finally: 
    # This code runs on every exit and sets any used GPIO pins to input mode.
    GPIO.cleanup()