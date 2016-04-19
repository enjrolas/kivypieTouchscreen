from kivy.app import App
from kivy.uix.widget import Widget
import OSC
import time

multicastAddress="224.0.0.1"  #multitouch
directAddress="10.0.1.8"  #alex
#directAddress="10.0.1.23"  #dez

multicastPort=7000
directPort=8000

width=2000
height=800

client=OSC.OSCClient()
multicastClient=OSC.OSCClient()

lastDirectClientAttempt=0
lastMulticastClientAttempt=0

reconnectAttempt=5  #try to connect every 5 seconds

class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        oscmsg=OSC.OSCMessage()
        oscmsg.setAddress("/touchDown")
        oscmsg.append(touch.uid)
        oscmsg.append(float(touch.x)/width)
        oscmsg.append(float(touch.y)/height)
        sendDirectMessage(oscmsg)
        sendMulticastMessage(oscmsg)


    def on_touch_move(self, touch):
        oscmsg=OSC.OSCMessage()
        print("%f %f" % (touch.x, touch.y))
        oscmsg.setAddress("/touchMove")
        oscmsg.append(touch.uid)
        oscmsg.append(float(touch.x)/width)
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
                connectDirectClient()
    
def sendMulticastMessage(oscmsg):        
        try:
            multicastClient.send(oscmsg)
        except:
            if (time.time()-lastMulticastClientAttempt)>reconnectAttempt:
                connectMulticastClient()
                
def connectDirectClient():
    print("connecting direct client to %s on port %d" % (directAddress, directPort))
    lastDirectClientAttempt=time.time()
    client.connect((directAddress, directPort))

def connectMulticastClient():
    print("connecting multicast client to %s on port %d" % (multicastAddress, multicastPort))
    lastMulticastClientAttempt=time.time()
    multicastClient.connect((multicastAddress, multicastPort))
                
def dump(obj):
    for attr in dir(obj):
        print("obj.%s \ %s" % (attr, getattr(obj, attr)))

class MyPaintApp(App):
    def build(self):
        return MyPaintWidget()


if __name__ == '__main__':
    connectDirectClient()
    connectMulticastClient()
    MyPaintApp().run()
