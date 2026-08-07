from groq import Groq
client=Groq(
api_key="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"
)
completion=client.chat.completions.create(
  model="llama-3.3-70b-versatile",
  messages=[
  {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and google cloud"},
  {"role": "user", "content": "what is coding"}
 ]
)
print(completion.choices[0].message.content)