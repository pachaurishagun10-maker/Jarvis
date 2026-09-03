import subprocess
import sys

print("=== Testing pyttsx3 ===")
try:
    import pyttsx3
    engine=pyttsx3.init('sapi5')
    engine.setProperty('rate',175)
    engine.setProperty('volume',1.0)
    engine.say("Testing pyttsx3 voice input.Can you hear me?")
    engine.runAndWait()
    print("pyttsx3 completed (did you hear audio?)")
except Exception as e:
    print(f"pyttsx3 failed: {e}")