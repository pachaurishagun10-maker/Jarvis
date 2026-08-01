import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer=sr.Recognizer()
engine=pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__=="__main__":
    speak("Initializing Jarvis.....")  #It'll speak this text when listen for the wake word"Jarvis"
    while True:
        r=sr.Recognizer()
        with sr.Microphone() as source: #obtain audio from microphone.
            print("Listening....")
            audio=r.listen(source)
    #Recognize speech using Sphinx
        try:
         command=r.recognize_sphinx(audio)
         print(command)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))