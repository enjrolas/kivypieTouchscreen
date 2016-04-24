from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.clock import Clock
import OSC
import time
import RPi.GPIO as GPIO


multicastAddress="224.0.0.1"  #multitouch
#directAddress="10.0.1.8"  #alex
directAddress="192.168.2.30"  #alex
#directAddress="10.0.1.23"  #dez

#Set GPIO mode
GPIO.setmode(GPIO.BCM)

#Setup GPIO
buttonPin=27
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #bottom

lastPressed=True
pressed=False
pressTime=0
debounce=0.25

frontMulticastPort=7000
frontDirectPort=8000
rearMulticastPort=7001
rearDirectPort=8001

multicastPort=frontMulticastPort
directPort=frontDirectPort


frontSide=True
side="front touchscreen"

width=800
height=800

client=OSC.OSCClient()
multicastClient=OSC.OSCClient()

lastDirectClientAttempt=0
lastMulticastClientAttempt=0

reconnectAttempt=5  #try to connect every 5 seconds

class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        oscmsg=OSC.OSCMessage()
        print("%s:  new touch at at %f %f" % (side, touch.x, touch.y))
        oscmsg.setAddress("/touchDown")
        oscmsg.append(touch.uid)
        oscmsg.append((width-float(touch.x))/width)
        oscmsg.append(float(touch.y)/height)
        sendDirectMessage(oscmsg)
        sendMulticastMessage(oscmsg)


    def on_touch_move(self, touch):
        oscmsg=OSC.OSCMessage()
        print("%s:  touch moved at %f %f" % (side, touch.x, touch.y))
        oscmsg.setAddress("/touchMove")
        oscmsg.append(touch.uid)
        oscmsg.append((width-float(touch.x))/width)
        oscmsg.append(float(touch.y)/height)
        try:
            oscmsg.append(touch.shape.width)
            oscmsg.append(touch.shape.height)
        except:
            oscmsg.append(0.0)
            oscmsg.append(0.0)
        sendDirectMessage(oscmsg)
        sendMulticastMessage(oscmsg)
        
    def on_touch_up(self, touch):
        oscmsg=OSC.OSCMessage()
        print("%s:  touch up at %f %f" % (side, touch.x, touch.y))
        oscmsg.setAddress("/touchUp")
        oscmsg.append(touch.uid)
        oscmsg.append(float(touch.x)/width)
        oscmsg.append(float(touch.y)/height)
        sendDirectMessage(oscmsg)
        sendMulticastMessage(oscmsg)
        

def sendDirectMessage(oscmsg):
        try:
            client.send(oscmsg)
        except:
            if (time.time()-lastDirectClientAttempt)>reconnectAttempt:
#                print "%d %d %d" % (time.time(), lastDirectClientAttempt, time.time()-lastDirectClientAttempt)
                connectDirectClient(directAddress, directPort)
    
def sendMulticastMessage(oscmsg):        
        try:
            multicastClient.send(oscmsg)
        except:
            if (time.time()-lastMulticastClientAttempt)>reconnectAttempt:
                connectMulticastClient(multicastAddress, multicastPort)
                
def connectDirectClient(directAddress, directPort):
    global lastDirectClientAttempt
    print("connecting to direct client to %s on port %d %f" % (directAddress, directPort, time.time()-lastDirectClientAttempt))
    lastDirectClientAttempt=time.time()
    try:
        client.connect((directAddress, directPort))
    except:
        print "had a problem connecting"

def connectMulticastClient(multicastAddress, multicastPort):
    print("connecting multicast client to %s on port %d" % (multicastAddress, multicastPort))
    lastMulticastClientAttempt=time.time()
    try:
        multicastClient.connect((multicastAddress, multicastPort))
    except:
        print "had a problem connecting"
                
def dump(obj):
    for attr in dir(obj):
        print("obj.%s \ %s" % (attr, getattr(obj, attr)))

def updateSide():
    global directPort, multicastPort, side
    if(frontSide):
        directPort=frontDirectPort
        multicastPort=frontMulticastPort
        side="front touchscreen"
    else:
        directPort=rearDirectPort
        multicastPort=rearMulticastPort
        side="rear touchscreen"
    connectDirectClient(directAddress, directPort)
    connectMulticastClient(multicastAddress, multicastPort)

class MyPaintApp(App):
    def build(self):
        # Instantiate the first UI object (the GPIO input indicator):
        inputDisplay = InputButton(text="Input")

        # Schedule the update of the state of the GPIO input button:
        Clock.schedule_interval(inputDisplay.update, 1.0/10.0)
        return MyPaintWidget()


# Modify the Button Class to update according to GPIO input:
class InputButton(Button):
    lastPressed=False
    pressed=False
    pressTime=0
    debounce=0.25    
    def update(self, dt):
        global frontSide
        self.pressed=GPIO.input(buttonPin)
        if self.pressed==False and self.lastPressed==True and time.time()>=(self.pressTime+self.debounce):
            self.pressTime=time.time()
            frontSide=not frontSide
            print("front:  %d" % frontSide)
            updateSide()
        self.lastPressed=self.pressed


if __name__ == '__main__':
    connectDirectClient(directAddress, directPort)
    connectMulticastClient(multicastAddress, multicastPort)
    MyPaintApp().run()
