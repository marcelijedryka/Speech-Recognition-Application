import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import pyttsx3 as tts


def run():

    global client , engine , messages
    messages = []
    engine = tts.init()
    engine.setProperty('volume',0.7)
    engine.setProperty('rate',190)
    client = mqtt.Client()
    client.on_message = message_recieved
    client.connect("localhost", 1883)
    client.subscribe("msg/spk")
    window = tk.Tk()
    window.title("Subscriber")
    label = tk.Label(text="Hello, I'm Subscriber, press the button to see if you got any messages")
    button = tk.Button(text="Get message" , command = read_messages)
    close_button = tk.Button(text="Close", command=quit)
    label.pack()
    button.pack()
    close_button.pack()
    client.loop_start()
    window.mainloop()
    client.loop_stop()

def message_recieved(client, userdata, message):
    print("I've recieved new message")
    msg = message.payload.decode()
    messages.append(msg)

def read_messages():

    if len(messages) == 0:
        messagebox.showinfo(title="Message reader info", message = "There are no new messages to read")
        
    else:
    
        for msg in messages:
            engine.say("New Message")
            engine.runAndWait()
            engine.say(msg)
            engine.runAndWait()
        messages.clear()

run()