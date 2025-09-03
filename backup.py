"This is a backup of the main assistant script. It is for me to refer to in case I mess up the main script."
"Just in case I mess up the main script."

import pyttsx4
import speech_recognition as sr
import datetime
import wikipedia
from duckduckgo_search import DDGS
import json
import sys
import os
import smtplib

# =======================
# SPEECH ENGINE
# =======================
engine = pyttsx4.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)  # Change index for different voices
engine.setProperty("rate", 175)

def speak(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# =======================
# GREETING
# =======================
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Jarvis Sir. Please tell me how may I help you")

# =======================
# VOICE INPUT
# =======================
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again please...")
        return "none"
    return query.lower()

# =======================
# WIKIPEDIA SEARCH
# =======================
def wiki_search(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except:
        speak("Sorry, I couldn't find information on Wikipedia.")

# =======================
# WEB SEARCH (DuckDuckGo)
# =======================
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results:
                title = results[0]["title"]
                body = results[0]["body"]
                link = results[0]["href"]
                speak(f"Here’s what I found: {title}. {body}")
                print(f"[INFO] {title}\n{body}\n{link}")
            else:
                speak("Sorry, I couldn’t find any results.")
    except Exception as e:
        print(f"[ERROR web_search]: {e}")
        speak("Sorry, web search is not available right now.")

def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-app-password')  # <-- Replace with your Gmail + app password
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        return True
    except Exception as e:
        print(f"[ERROR Email]: {e}")
        return False

def matches(query, keywords):
    return any(word in query.split() for word in keywords)

# =======================
# LOAD SCRIPTED CHAT
# =======================
with open("chat_script.json", "r") as f:
    scripted_responses = json.load(f)

def chat_mode():
    speak("Entering chat mode. Say 'exit chat' to stop.")
    while True:
        user_msg = take_command()
        if "exit chat" in user_msg:
            speak("Exiting chat mode.")
            break

        reply = None
        for key in scripted_responses:
            if key in user_msg:
                reply = scripted_responses[key]
                break

        if reply:
            speak(reply)
        else:
            speak("Sorry, I don’t know how to respond to that yet.")

# =======================
# MAIN PROGRAM LOOP
# =======================
if __name__ == "__main__":
    wish_user()

    while True:
        query = take_command().strip()

        if query == "none":
            continue

        print(f"[DEBUG] Final query: {query}")

        # EXIT HAS TOP PRIORITY AND BREAKS LOOP
        if "exit" == query or "quit" == query or "close" == query or "stop" == query or "shutdown" == query:
            speak("Goodbye, have a great day!")
            break   # <-- instead of sys.exit (cleaner exit from loop)

        elif "wikipedia" in query:
            topic = query.replace("wikipedia", "").strip()
            speak("Searching Wikipedia...")
            wiki_search(topic)

        elif "search" in query:
            topic = query.replace("search", "").strip()
            if topic:
                speak(f"Searching the web for {topic}")
                web_search(topic)
            else:
                speak("Please tell me what to search.")

        elif "chat mode" in query:
            chat_mode()

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {strTime}")

        elif "date" in query:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}")

        elif "email to harry" in query:
            try:
                speak("What should I say?")
                content = take_command()
                to = "harryyourEmail@gmail.com"
                if sendEmail(to, content):
                    speak("Email has been sent!")
                else:
                    speak("Sorry, I couldn’t send the email right now.")
            except Exception as e:
                print(e)
                speak("Sorry my friend Harry bhai. I am not able to send this email.")

        elif "send email" in query:
            try:
                speak("What should I say?")
                content = take_command()
                speak("Whom should I send it to? Please provide the email address.")
                to = take_command()

                if sendEmail(to, content):
                    speak("Email has been sent successfully.")
                else:
                    speak("Sorry, I was unable to send the email.")
            except Exception as e:
                print(e)
                speak("Sorry, I was not able to send the email.")

        else:
            speak("I'm sorry, I didn't understand that. Could you please repeat?")

