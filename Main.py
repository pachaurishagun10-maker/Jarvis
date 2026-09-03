import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLibrary
import requests
import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

recognizer = sr.Recognizer()
engine = pyttsx3.init()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_CITY = os.getenv("WEATHER_CITY", "Jaipur")

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def aiProcess(command):

    client = Groq(
        api_key=GROQ_API_KEY
    )

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a virtual assistant named Jarvis. "
                    "You are helpful, intelligent and concise."
                )
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content


def getNews():

    if not NEWS_API_KEY:
        speak("News API key is missing.")
        print("ERROR: NEWS_API_KEY not found in .env")
        return

    try:

        url = (
            "https://newsapi.org/v2/top-headlines"
            f"?country=in&apiKey={NEWS_API_KEY}"
        )

        response = requests.get(url, timeout=10)

        print("News API Status:", response.status_code)

        if response.status_code == 200:

            data = response.json()

            articles = data.get("articles", [])

            if not articles:
                speak("I couldn't find any news right now.")
                return

            speak("Here are the latest news headlines.")

            for article in articles[:5]:

                title = article.get("title")

                if title:
                    print("News:", title)
                    speak(title)

        else:

            print("News API Response:", response.text)

            speak(
                "Sorry, I couldn't get the latest news."
            )

    except requests.exceptions.RequestException as e:

        print("News request error:", e)

        speak(
            "Sorry, I couldn't connect to the news service."
        )

    except Exception as e:

        print("News error:", e)

        speak(
            "Something went wrong while getting the news."
        )


def getWeather():

    if not WEATHER_API_KEY:
        speak("Weather API key is missing.")
        print("ERROR: WEATHER_API_KEY not found in .env")
        return

    try:

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric"
        )

        response = requests.get(url, timeout=10)

        print("Weather API Status:", response.status_code)

        if response.status_code == 200:

            data = response.json()

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            city = data["name"]

            message = (
                f"The weather in {city} is {description} "
                f"with a temperature of {temp} degrees Celsius, "
                f"feels like {feels_like} degrees."
            )

            print("Weather:", message)
            speak(message)

        else:

            print("Weather API Response:", response.text)
            speak("Sorry, I couldn't get the weather right now.")

    except requests.exceptions.RequestException as e:

        print("Weather request error:", e)
        speak("Sorry, I couldn't connect to the weather service.")

    except Exception as e:

        print("Weather error:", e)
        speak("Something went wrong while getting the weather.")


def processCommand(c):

    c = c.lower().strip()


    if "open google" in c:

        speak("Opening Google...")
        webbrowser.open("https://www.google.com")


    elif "open youtube" in c:

        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")


    elif "open github" in c:

        speak("Opening GitHub...")
        webbrowser.open("https://github.com")


    elif "open chatgpt" in c:

        speak("Opening ChatGPT...")
        webbrowser.open("https://chatgpt.com") 


    elif c.startswith("play"): 

        parts = c.split() 

        if len(parts) < 2: 

            speak("Please tell me which song you want to play.") 

        else: 

            song = parts[1] 

            if song in MusicLibrary.Music: 

                link = MusicLibrary.Music[song] 

                speak(f"Playing {song}...") 

                webbrowser.open(link) 

            else: 

                speak("Sorry, I don't have that song in my music library.") 


    elif "news" in c: 

        getNews() 

    elif "weather" in c: 

        getWeather()     

    else: 

        output = aiProcess(c) 

        print("Jarvis:", output) 

        speak(output) 

if __name__ == "__main__": 

    speak("Activating Jarvis") 

    while True: 

        try: 

            with sr.Microphone() as source: 

                print("Recognizing...") 

                recognizer.adjust_for_ambient_noise( 
                    source, 
                    duration=0.8 
                ) 

                audio = recognizer.listen( 
                    source, 
                    timeout=7, 
                    phrase_time_limit=5 
                ) 


            print("Processing...") 

            word = recognizer.recognize_google(audio) 

            print(f"Heard: {word}") 


            if "jarvis" in word.lower(): 

                remaining = ( 
                    word.lower() 
                    .replace("jarvis", "") 
                    .strip() 
                ) 
                 
                if remaining: 

                    print(f"Command: {remaining}") 

                    processCommand(remaining) 


                else: 

                    speak("Yes") 

                    try: 

                        with sr.Microphone() as source: 

                            print("Listening...") 

                            recognizer.adjust_for_ambient_noise( 
                                source, 
                                duration=0.5 
                            ) 

                            audio = recognizer.listen( 
                                source, 
                                timeout=7, 
                                phrase_time_limit=5 
                            ) 


                        command = recognizer.recognize_google(audio) 

                        print(f"Command: {command}") 

                        processCommand(command) 


                    except sr.WaitTimeoutError: 

                        print("Timeout - Can't hear") 


                    except sr.UnknownValueError: 

                        print("Didn't understand what you said") 


                    except Exception as e: 

                        print(f"Command error: {e}") 


        except sr.WaitTimeoutError: 

            print("Timeout - Can't hear") 


        except sr.UnknownValueError: 

            print("Didn't understand what you said") 


        except Exception as e: 

            print(f"Error: {e}")