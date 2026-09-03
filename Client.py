import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def aiProcess(command):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )

    return completion.choices[0].message.content