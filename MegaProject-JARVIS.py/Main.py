import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLibrary
import requests
from groq import Groq
import pygame
pygame.mixer.init()
recognizer=sr.Recognizer()
engine=pyttsx3.init('sapi5')

def play_sound(file):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiprocess(c):
    client=Groq(
        api_key="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"
    )
    completion=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and google cloud"},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content
    
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

    elif "news" in c.lower():
        newsapi="39d0c5dcc136403b8c20772e1287b4fe"
        r=requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code==200:
            data=r.json() #Parse the JSON response
            articles=data.get('articles',[]) #Extract the articles
            for article in articles:   #Print the headlines
                speak(article['title'])

    else:
        output=aiprocess(c)
        speak(output)


if __name__=="__main__":
    speak("Initializing Jarvis.....")  #It'll speak this text when listen for the wake word"Jarvis"
    r=sr.Recognizer() #Adjust background noice
    r.dyanamic_energy_threshold=True
    r.pause_threshold=1

    while True:
        try:
            with sr.Microphone() as source: #obtain audio from microphone.
               print("Listening....")
               r.adjust_for_ambient_noise(source,duration=1)
               audio=r.listen(source,timeout=5,phrase_time_limit=3)
            word=r.recognize_google(audio)
            print(f"Heard: {word}")

            if(word.lower()=="jarvis"):
                speak("Yes")
                #Listen for command

                with sr.Microphone() as source: #obtain audio from microphone.
                    print("Jarvis is now active..")
                    r.adjust_for_ambient_noise(source,duration=1)
                    audio=r.listen(source,timeout=8,phrase_time_limit=8)
                    command=r.recognize_google(audio)
                    print(f"Command: {command}")
                    processcommand(command)
        except Exception as e:
            print("Error; {0}".format(e)) 