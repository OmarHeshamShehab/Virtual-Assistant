import os
from pickle import TRUE

import openai
import pyaudio
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")


openai.api_key = OPENAI_KEY


# Function to convert text to speech
def SpeakText(command):
    # initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


# initialize the recognizer
r = sr.Recognizer()


def record_text():
    # looping on errors
    while TRUE:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.1)
                print("I'm listening")
                user_audio = r.listen(source)
                MyText = r.recognize_google(user_audio)
                return MyText

        except sr.RequestError as err:
            print(f"could not request results {err}")
        except sr.UnknownValueError:
            print("unknown error occurred")


def send_to_ChatGPT(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model, messages=messages, max_tokens=100, n=1, stop=None, temperature=0.5
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


messages = []
while True:
    text = record_text()
    messages.append({"role": "user", "content": text})
    response = send_to_ChatGPT(messages)
    SpeakText(response)

    print(response)
