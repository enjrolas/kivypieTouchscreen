from kivy.app import App
from kivy.uix.widget import Widget
import OSC
import time

#address="224.0.0.1"  #multitouch
address="10.0.1.8"  #direct

port=7000

width=1200
height=800

client=OSC.OSCClient()
client.connect((address, port))


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        oscmsg=OSC.OSCMessage()
        oscmsg.setAddress("/newTouch")
        oscmsg.append(touch.uid)
        oscmsg.append(float(touch.x)/width)
        oscmsg.append(float(touch.y)/height)
        client.send(oscmsg)


    def on_touch_move(self, touch):
        oscmsg=OSC.OSCMessage()
        oscmsg.setAddress("/touch")
        oscmsg.append(touch.uid)
        oscmsg.append(float(touch.x)/width)
        oscmsg.append(float(touch.y)/height)
        try:
            oscmsg.append(touch.shape.width)
            oscmsg.append(touch.shape.height)
        except:
            oscmsg.append(0.0)
            oscmsg.append(0.0)
        client.send(oscmsg)

    def on_touch_up(self, touch):
        oscmsg=OSC.OSCMessage()
        oscmsg.setAddress("/touchUp")
        oscmsg.append(touch.uid)
        oscmsg.append(float(touch.x)/width)
        oscmsg.append(float(touch.y)/height)
        client.send(oscmsg)

                
def dump(obj):
    for attr in dir(obj):
        print("obj.%s \ %s" % (attr, getattr(obj, attr)))

class MyPaintApp(App):
    def build(self):
        return MyPaintWidget()


if __name__ == '__main__':
    MyPaintApp().run()
