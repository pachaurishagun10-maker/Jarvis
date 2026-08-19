import speech_recognition as sr
import win32com.client
import webbrowser
import pyttsx3
import MusicLibrary
import requests
from groq import Groq
import urllib.parse
from datetime import datetime 

GROQ_API_KEY="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"
NEWS_API_KEY="39d0c5dcc136403b8c20772e1287b4fe"

TTS_METHOD="sapi"

def speak(text):
    """Speak the given text aloud AND display it on the screen"""
    global TTS_METHOD
    print(f"\n JARVIS : {text}\n")
    clean_text=str(text).replace("°","degrees").replace("%","percent")

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

    if TTS_METHOD=="pyttsx3":
        try:
            engine=pyttsx3.init('sapi5')
            engine.setProperty('rate,175')
            engine.setProperty('volume,1.0')
            engine.say(clean_text)
            engine.runAndWait()
        except Exception as e:
            print(f"[!] pyttsx3 error: {e}")

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
                for topic in data["RelatedTopics"][:3]:
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
            return f"Could not fetch weather data for {City}."
    except Exception as e:
        return f" Weather service error: {e}"
    
def get_news():
    """Fetch top news headlines using NewsAPI"""
    try:
        url=f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API_KEY}"
        response=requests.get(url,timeout=10)
        if response.status_code==200:
            data=response.json()
            articles=data.get('articles',[])

            if articles:
                headlines=[]
                for i,article in enumerate(articles[:5],1):
                    title=article.get('title','No title')
                    headlines.append(f"Headline {i}: {title}")
                    print(f" [News] Headline {i}: {title}")
                return headlines
            return ["No news articles found."]
        return [f"News API returned status{response.status_code}"]
    except Exception as e:
            return[f"News error: {e}"]

def processcommand(command):
    """Process the recognized voice command and execute actions."""
    c=command.lower().strip()
    print(f"\n{'='*50}\nYOUR COMMAND:{command}\n{'='*50}")

    if "open Google" in c:
        speak("Opening Google...")
        webbrowser.open("https://www.Google.com")
    
    elif "open Youtube" in c:
        speak("Opening Youtube...")
        webbrowser.open("https://www.Youtube.com")
    
    elif "open Github" in c:
        speak("Opening Github...")
        webbrowser.open("https://www.Github.com")
    
    elif "open chatgpt" in c:
        speak("Opening chatgpt ...")
        webbrowser.open("https://www.chat.openai.com")    
    elif c.startswith("open"):
        site_name=c.replace("open"," ").strip()
        site_name=site_name.replace(" ","")
        url=f"https://www.{site_name}.com"
        speak(f"Opening {site_name} for you.")
        webbrowser.open(url)
    elif c.startswith("play"):
        song=c.replace("play","").strip()
        matched_song=None
        if song in MusicLibrary.Music:
            matched_song=song
        else:
            song_nospace=song.replace(" ","")
            for lib_song  in MusicLibrary.Music:
                if lib_song.replace(" ",""==song_nospace):
                    matched_song=lib_song 
                    break
        if matched_song:
            speak(f"Playing {matched_song} for you.")
            webbrowser.open(MusicLibrary.Music[matched_song])
        else:
            speak(f"Searching {song} on Youtube")
            search_url=f"https://www.youtube.com/results?search_query={urllib.parse.quote(song)}"
            webbrowser.open(search_url)

    elif "news" in c:
        speak("Fetching the latest news headlines for you.")
        headlines=get_news()
        for headline in headlines[:5]:
            speak(headline)

    elif "weather" in c:
        city="Jaipur" 
        weather_patterns= ["weather in","weather of","weather for"]
        for pattern in weather_patterns:
            if pattern in c:
                city=c.split(pattern)[1].strip()
                break
        result = get_weather(city)
        speak(result)

    elif "time" in c:
        current_time=datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in c or "today" in c and "what" in c:
        current_date=datetime.now().strftime("%B %d,%Y")
        speak(f"Today's date is {current_date}") 

    elif any(word in c for word in ["stop","exit","bye","goodbye"]):
        speak("Goodbye! Shutting down Jarvis.")
        exit(0)
        
    else:
        speak("Let me think about that...")
        result=aiprocess(command)
        speak(result)

if __name__=="__main__":
    print("\n" + "=" *60)
    print("JARVIS AI VOICE ASSISTANT-Enhanced Edition")
    print(" " + "=" *56)
    print("Say 'Jarvis' to activate, then give your command")
    print("Commands:open[website],play[song],news")
    print("weather,search[topic],or ask anything!")
    print("Say 'Stop' or 'Exit' to quit")
    print("=" * 60 + "\n")
    speak("Initializing Jarvis.I am ready to asisst you.")
    r=sr.Recognizer()
    r.dynamic_energy_threshold = True 
    r.pause_threshold=1

    while True:
        try:
            with sr.Microphone() as source:
                print("\n Listening for wake word 'Jarvis'...")
                r.adjust_for_ambient_noise(source,duration=0.5)
                audio=r.listen(source,timeout=5,phrase_time_limit=5)
            word=r.recognize_google(audio)
            print(f"Heard:{word}")

            if "Jarvis" in word.lower():
                speak("Yes,I'm listening. What can i do for you?")
                print("listening for your command...")

                with sr.Microphone() as source:
                    print("\n JARVIS IS ACTIVE-Speak your command...")
                    r.adjust_for_ambient_noise(source,duration=0.5)
                    audio=r.listen(source,timeout=10,phase_time_limit=10)
                    command=r.recognize_google(audio)
                    processcommand(command)
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e: 
            print(f" [!] Speech Recognition service error: {e}")
            print(" [!] Check your internet connection.")
        except KeyboardInterrupt:
            speak("Goodbye!")c
            break
        except Exception as e:
            print(f" [!] Error: {e}")