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
import random
import math
import time

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

kill = False

aim = Circle(Point(250, 250), 15)
target = Circle(Point(0, 0), 10)
message = Text(Point(100, 100), "")
scoreText = Text(Point(100, 50), "")
score = 0

win = GraphWin("Target Practice", SCREEN_WIDTH, SCREEN_HEIGHT, autoflush=False)

def getXPosition():
    global chan
    return round(chan.voltage/3.3 * SCREEN_WIDTH)

def getYPosition():
    global chan2
    return round(chan2.voltage/3.3 * SCREEN_HEIGHT)
    
def spawnTarget():
    global target
    global kill
    found = False
    target.undraw()
    while not found:
        target = Circle(Point(random.randint(20, SCREEN_WIDTH - 20), random.randint(20, SCREEN_HEIGHT - 20)), 10)
        targetCenter = target.getCenter()
        if math.sqrt((250 - targetCenter.x)**2 + (250 - targetCenter.y)**2) <= (260):
            found = True
    target.setFill("Blue")
    kill = False
    target.draw(win)

def shoot(channel):
    global target
    global aim
    global kill
    global score
    aimCenter = aim.getCenter()
    targetCenter = target.getCenter()
    
    if math.sqrt((aimCenter.x - targetCenter.x)**2 + (aimCenter.y - targetCenter.y)**2) <= (25):
        kill = True
        score += 1

def main():
    global aim
    global target
    global kill
    global score
    
    # set coordnate plane for easy translation from the joystick position
    # xll, yll, xur, yur
    win.setCoords(SCREEN_WIDTH, 0, 0, SCREEN_HEIGHT)
    win.setBackground("Grey")
    
    message.setTextColor("white")
    message.setSize(20)
    message.draw(win)
    
    scoreText.setTextColor("white")
    scoreText.setSize(20)
    scoreText.draw(win)
    
    target.draw(win)
    spawnTarget()
    
    aim.draw(win)
    
    end = time.time() + 30
    playing = True
    while(playing):
        timeLeft = round(end - time.time(), 2)
        if timeLeft <= 0:
            message.setText("Game Over!")
            scoreText.setText("Final Score: " + str(score))
            playing = False
        else:
            message.setText(timeLeft)
            scoreText.setText("Score: " + str(score))
            if kill:
                spawnTarget()
            aim.undraw()
            aim = Circle(Point(getXPosition(), getYPosition()), 15)
            aim.setFill("Red")
            aim.draw(win)
            
        update(60)
    
    time.sleep(5)
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

try:
    main()

except KeyboardInterrupt: 
    # This code runs on a Keyboard Interrupt <CNTRL>+C
    print('\n\n' + 'Program exited on a Keyboard Interrupt' + '\n') 

except: 
    # This code runs on any error
    print('\n' + 'Errors occurred causing your program to exit' + '\n')

finally: 
    # This code runs on every exit and sets any used GPIO pins to input mode.
    GPIO.cleanup()