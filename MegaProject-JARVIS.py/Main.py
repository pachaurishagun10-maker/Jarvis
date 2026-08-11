import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLibrary
import requests
from groq import Groq
import os
import re
import json
import subprocess
import urllib.parse
from datetime import datetime 
GROQ_API_KEY="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"
NEWS_API_KEY="39d0c5dcc136403b8c20772e1287b4fe"

TTS_METHOD="pyttsx3"

try:
    import win32com.client
    _test_speaker=win32com.client.Dispatch("SAPI.SpVoice")
    TTS_METHOD="sapi"
    print("[TTS] Using Windows SAPI (win32com)-best quality")
except Exception:
    try:
        engine=pyttsx3.init('sapi5')
        engine.setProperty('rate',175)
        engine.setproperty('volume',1.0)
        TTS_METHOD="pyttsx3"
        print("[TTS] Using pyttsx3")
    except Exception:
        TTS_METHOD="powershell"
        print("[TTS] Using PowerShell fallback")
recognizer=sr.Recognizer()

def speak(text):
    """Speak the given text aloud AND display it on the screen"""
    global TTS_METHOD
    print(f"\n JARVIS : {text}\n")
    clean_text=text.replace('°','degrees').replace('%','percent')

    if TTS_METHOD=="sapi":
        try:
            speaker=win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Rate=1
            speaker.Volume=100
            speaker.Speak(clean_text)
            return
        except Exception as e:
            print(f" [!] SAPI error: {e}, trying pyttsx3...")
            TTS_METHOD="pyttsx3"
def aiprocess(command_text):
    """Send a command to the Groq AI and get a response"""
    try:
        client=Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role":"system",
                    "content":(
                        "You are a virtual assistant named JARVIS,skilled in general tasks"
                        "You are helpful,creative,intelligent,and give concise answers to questions"
                    )
              },
              {"role":"user", "content":command_text}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Sorry, I couldn't process that command.Error:{e}"

def google_search(query):
    """Search Google and return top results using DuckDuckGo instant answer API"""
    try:
        url=f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
        response=requests.get(url,timeout=10)
        if response.status_code==200:
            data=response.json()
            if data.get("AbstractText"):
                return data["AbstractText"]
            if data.get("Answer"):
                return data["Answer"]
            if data.get("RelatedTopics") and len(data["RelatedTopics"])>0:
                results=[]
                for topic in data["RealtedTopics"][:3]:
                    if isinstance(topic,dict) and topic.get("Text"):
                        results.append(topic["Text"])
                if results:
                    return "|".join(results)
                return None
    except Exception as e:
            print(f" [!] Search error: {e}")
            return None

def get_weather(City="Jaipur"):
    """Get weather info using wttr.in"""
    try:
        url=f"https://wttr.in/{urllib.parse.quote(City)}?format=j1"
        response=requests.get(url,timeout=10)
        if response.status_code==200:
            data=response.json()
            current=data["current_condition"][0]
            temp=current["temp_C"]
            desc=current["weatherDesc"][0]["value"]
            humidity=current["humidity"]