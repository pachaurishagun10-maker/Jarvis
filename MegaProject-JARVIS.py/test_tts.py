import subprocess
import sys

print("=== Testing pyttsx3 ===")
try:
    import pyttsx3
    engine=pyttsx3.init('sapi5')
    engine.setProperty('rate',175)
    engine.setproperty('volume',1.0)
    engine.say
