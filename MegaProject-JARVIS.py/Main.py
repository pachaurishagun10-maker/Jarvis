import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLibrary
import requests
from groq import Groq
recognizer=sr.Recognizer()
engine=pyttsx3.init('sapi5')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(command):
    import Client
    completion=Client.completion
    response=completion.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and google cloud"},
            {"role": "user", "content": command}
        ]
    )
    return response.choices[0].message.content
    
def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com")
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=MusicLibrary.Music[song]
        webbrowser.open(link)
        
if __name__=="__main__":
    speak("Initializing Jarvis.....")  #It'll speak this text when listen for the wake word"Jarvis"
    while True:
        r=sr.Recognizer()

        print("Recognizing....")
        try:
            with sr.Microphone() as source: #obtain audio from microphone.
               print("Listening....")
               audio=r.listen(source,timeout=3,phrase_time_limit=3)
            word=r.recognize_google(audio)
            if(word.lower()=="jarvis"):
                speak("Yes")
                #Listen for command
                with sr.Microphone() as source: #obtain audio from microphone.
                    print("Jarvis is now active..")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)
                    processcommand(command)
        except Exception as e:
            print("Error; {0}".format(e)) 