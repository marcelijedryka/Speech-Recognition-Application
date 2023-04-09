import tkinter as tk
from tkinter import messagebox
import paho.mqtt.client as mqtt
import speech_recognition as sr


def run():

    global client
    global window
    client = mqtt.Client()
    window = tk.Tk()
    window.title("Publisher")
    label = tk.Label(text="Hello, I'm Publisher, press the button and say your message")
    button = tk.Button(text="Start" , command=new_message)
    close_button = tk.Button(text="Close", command=quit)
    label.pack()
    button.pack()
    close_button.pack()
    window.mainloop()

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
    print("Recieving new message")

    msg = get_msg()
        
    if msg:
        client.connect("localhost" , 1883)
        client.publish("msg/spk" , msg)
        client.disconnect()
    else:
        messagebox.showwarning("Warning", "No message has been recieved")

run()



