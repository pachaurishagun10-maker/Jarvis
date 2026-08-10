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
