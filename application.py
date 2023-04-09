import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import speech_recognition as sr
import pyttsx3 as tts

def run():

    global client , engine , window , messages
    global window
    messages = []
    engine = tts.init()
    engine.setProperty('volume',0.7)
    engine.setProperty('rate',190)
    client = mqtt.Client()
    client.on_message = message_recieved
    client.connect("localhost", 1883)
    client.subscribe("msg/spk")
    window = tk.Tk()
    window.title("My Application")
    label = tk.Label(text="Press the button below to send your message")
    button = tk.Button(text="Start" , command=new_message)
    label2 = tk.Label(text="Press the button below read your messages")
    button2 = tk.Button(text="Get message" , command = read_messages)
    close_button = tk.Button(text="Close", command=quit)
    label.pack()
    button.pack()
    label2.pack()
    button2.pack()
    close_button.pack()
    client.loop_start()
    window.mainloop()
    client.loop_stop()

def get_msg():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        audio = r.listen(source)

        try:
            tekst = r.recognize_google(audio, language='pl_PL')
            print(tekst)
            return tekst
        except sr.UnknownValueError:
            messagebox.showwarning("Warning", "Cannot recognize your message")

def new_message():
    print("Sending new message")

    msg = get_msg()
        
    if msg:
        client.publish("msg/spk" , msg)
    else:
        messagebox.showwarning("Warning", "No message has been recieved")

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