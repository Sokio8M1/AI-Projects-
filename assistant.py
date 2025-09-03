import pyttsx4
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
webbrowser.open("https://www.google.com")
import json
import threading
import time
import smtplib
import os

# ========== VOICE ENGINE ==========
engine = pyttsx4.init()
engine.setProperty("rate", 170)  # speaking speed

def speak(audio):
    print(f"Assistant: {audio}")
    engine.say(audio)
    engine.runAndWait()

# ========== GREETING ==========
def wish_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
        speak("I am Jarvis Sir. Please tell me how may I help you")
        
# ========== TESTER CHECKER ==========
def check_if_tester():
    speak("Are you a tester for this project? Please say yes or no.")
    answer = take_command().lower()

    if "yes" in answer:
        speak("Thank you for testing this assistant. Please share your views and suggestions after using it. Your feedback will help improve the project.")
        speak("A note from Sir: This project is still in its early stages and may have bugs. Please be patient and report any issues you encounter.")
        speak("Hello its me the coder , Bhaswar. So as you are a tester , Jarvis is going to guide you on how to use this assistant.     Hi Jarvis speaking , you can ask me to search anything on wikipedia by saying 'wikipedia' followed by the topic. You can also ask me to search anything on google by saying 'search' followed by the topic but I dont recite that . You can set reminders by saying 'set reminder' or 'remind me'. You can record tasks by saying 'record this task' or 'record this as a task'. You can ask me to list your tasks by saying 'tasks' or 'say what I have to do for today'. You can shift tasks by saying 'move task' or 'shift task' although the reminder feature is currently in dev mode and may not function perfectly. You can also ask me the current time by saying 'time' and the current date by saying 'date'. You can send emails by saying 'send email' but keep in mind it requires your account setup. If you want to exit, just say 'exit', 'quit', 'close', or 'stop'. I hope you have a great experience using this assistant. Thank you!")
    elif "no" in answer:
        speak("Welcome back sir. How can I assist you today?")
    else:
        speak("I didn't catch that. Please say yes or no.")
        check_if_tester()

# ========== LISTENING ==========
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"[DEBUG] You said: {query}")
            return query.lower()
        except Exception as e:
            print(f"[DEBUG] Recognition error: {e}")
            return "none"

# ========== EMAIL ==========
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        return True
    except Exception as e:
        print(e)
        return False

# ========== REMINDERS & TASKS ==========
import json, datetime, threading, time
import re

DATA_FILE = "assistant_data.json"

# ---------- Data Handling ----------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"reminders": [], "tasks": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def extract_number(text: str):
    text = text.lower().strip()
    
    # Direct digits (e.g., "2")
    match = re.search(r"\d+", text)
    if match:
        return int(match.group())

    # Common number words
    words_to_num = {
        "one": 1, "first": 1,
        "two": 2, "second": 2,
        "three": 3, "third": 3,
        "four": 4, "fourth": 4,
        "five": 5, "fifth": 5
    }
    for word, num in words_to_num.items():
        if word in text:
            return num

    return None


# ---------- Reminders ----------
import re

import re, datetime

def normalize_time_input(user_input: str) -> str:
    user_input = user_input.lower().strip()

    # Remove dots: "a.m." → "am"
    user_input = user_input.replace(".", "").replace("  ", " ")

    # --- Keyword-based AM/PM ---
    if "morning" in user_input:
        user_input = user_input.replace("morning", "").strip() + " AM"
    elif "afternoon" in user_input or "evening" in user_input or "night" in user_input:
        user_input = user_input.replace("afternoon", "").replace("evening", "").replace("night", "").strip() + " PM"

    # Normalize "7 am" → "7:00 AM"
    match = re.match(r"^(\d{1,2})(\s*am|\s*pm)?$", user_input, flags=re.IGNORECASE)
    if match:
        hour = match.group(1)
        suffix = match.group(2) if match.group(2) else ""
        user_input = f"{hour}:00 {suffix.upper()}".strip()

    return user_input.upper()
   

def parse_reminder_datetime(user_input: str):
    user_input = normalize_time_input(user_input)
    now = datetime.datetime.now()

    try:
        if "TODAY AT" in user_input:
            t = user_input.replace("TODAY AT", "").strip()
            rt = datetime.datetime.strptime(t, "%I:%M %p")
            return now.replace(hour=rt.hour, minute=rt.minute, second=0, microsecond=0)

        elif "TOMORROW AT" in user_input:
            t = user_input.replace("TOMORROW AT", "").strip()
            rt = datetime.datetime.strptime(t, "%I:%M %p")
            tomorrow = now + datetime.timedelta(days=1)
            return tomorrow.replace(hour=rt.hour, minute=rt.minute, second=0, microsecond=0)

        elif "AT" in user_input:
            date_part, time_part = user_input.split("AT")
            date_part, time_part = date_part.strip().title(), time_part.strip().upper()
            reminder_date = datetime.datetime.strptime(date_part, "%B %d").replace(year=now.year)
            rt = datetime.datetime.strptime(time_part, "%I:%M %p")
            return reminder_date.replace(hour=rt.hour, minute=rt.minute, second=0, microsecond=0)

        else:
            rt = datetime.datetime.strptime(user_input.upper(), "%I:%M %p")
            return now.replace(hour=rt.hour, minute=rt.minute, second=0, microsecond=0)

    except Exception as e:
        print(f"[DEBUG] Time parsing failed for '{user_input}': {e}")
        return None


def add_reminder(message, reminder_datetime):
    data = load_data()
    data["reminders"].append({
        "time": reminder_datetime.strftime("%Y-%m-%d %H:%M"),
        "message": message
    })
    save_data(data)
    speak(f"Reminder set for {reminder_datetime.strftime('%I:%M %p on %B %d')}: {message}")


def reminder_checker():
    while True:
        data = load_data()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for r in list(data["reminders"]):
            if r["time"] == now:
                speak(f"Reminder: {r['message']}")
                data["reminders"].remove(r)
                save_data(data)
        time.sleep(30)

# ---------- To-Do Tasks ----------
def add_task(task, date=None, time_str=None):
    data = load_data()
    if not date:
        date = datetime.date.today().strftime("%Y-%m-%d")

    task_entry = {"task": task, "date": date}

    if time_str:
        time_str = normalize_time_input(time_str)
        try:
            rt = datetime.datetime.strptime(time_str, "%I:%M %p")
            task_entry["time"] = rt.strftime("%H:%M")
        except Exception as e:
            print(f"[DEBUG] Failed to parse task time '{time_str}': {e}")

    data["tasks"].append(task_entry)
    save_data(data)

    msg = f"Task recorded for {date}"
    if "time" in task_entry:
        msg += f" at {task_entry['time']}"
    msg += f": {task}"
    speak(msg)


def list_tasks(date=None):
    data = load_data()
    if not date:
        date = datetime.date.today().strftime("%Y-%m-%d")
    tasks_today = [t for t in data["tasks"] if t["date"] == date]

    if not tasks_today:
        speak("You have no tasks for today.")
    else:
        speak("Your tasks for today are:")
        for idx, t in enumerate(tasks_today, 1):
            if "time" in t:
                speak(f"Task {idx}: {t['task']} at {t['time']}")
            else:
                speak(f"Task {idx}: {t['task']}")


def shift_task(task_number, new_date, new_time=None):
    data = load_data()
    tasks = data["tasks"]

    today = datetime.date.today().strftime("%Y-%m-%d")
    today_tasks = [t for t in tasks if t["date"] == today]

    if 0 < task_number <= len(today_tasks):
        task = today_tasks[task_number - 1]
        task["date"] = new_date

        if new_time:
            new_time = normalize_time_input(new_time)
            try:
                rt = datetime.datetime.strptime(new_time, "%I:%M %p")
                task["time"] = rt.strftime("%H:%M")
            except Exception as e:
                print(f"[DEBUG] Failed to parse shifted task time '{new_time}': {e}")

        save_data(data)
        msg = f"Task {task_number} has been moved to {new_date}"
        if "time" in task:
            msg += f" at {task['time']}"
        speak(msg)
    else:
        speak("Invalid task number.")

# ========== WIKI SEARCH ==========
def wiki_search(topic):
    try:
        results = wikipedia.summary(topic, sentences=2)
        speak("Searching Wikipedia...")
        speak("According to Wikipedia")
        speak(results)
    except Exception:
        speak("Sorry sir, I could not fetch information from Wikipedia.")

# ========== WEB SEARCH ==========
def web_search(query):
    try:
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        speak(f"Here’s what I found for {query} on Google.")
        webbrowser.open(url)
    except Exception:
        speak("Sorry sir, I was unable to perform a Google search.")

# ========== CHAT MODE ==========
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


# ========== MAIN ==========
if __name__ == "__main__":
    wish_user()
    speak("I am your personal assistant Jarvis. Please tell me how may I help you")
    #speak("If you think why Sir named me  Jarvis, its because he is a fan of Iron Man and his AI assistant Jarvis. Also he is a coder and love coding. So he probably would have thought , wait, why not name it Jarvis. Haha ha ")
    #check_if_tester()
    
    
    # Start background reminder checker
    threading.Thread(target=reminder_checker, daemon=True).start()
    
    while True:
        query = take_command().strip()

        if query == "none":
            continue

        # EXIT
        if query in ["exit", "quit", "close", "stop"]:
            speak("Goodbye, have a great day!.Hope to hear from you again.")
            break

        # WIKI
        elif "wikipedia" in query:
            topic = query.replace("wikipedia", "").strip()
            wiki_search(topic)

        # SEARCH
        elif "search" in query:
            topic = query.replace("search", "").strip()
            if topic:
                speak(f"Searching the web for {topic}")
                web_search(topic)
            else:
                speak("Please tell me what to search.")

        # TIME
        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {strTime}")
            speak("Is there anything else you want me to do for you sir?")

        # DATE
        elif "date" in query:
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {today}")
            speak("Is there anything else you want me to do for you sir?")

        # EMAIL
        elif "email to boss" in query:
            try:
                speak("What should I say?")
                content = take_command()
                to = "harryyourEmail@gmail.com"
                if sendEmail(to, content):
                    speak("Email has been sent!")
                    speak("Is there anything else you want me to do for you sir?")
                else:
                    speak("Sorry, I couldn’t send the email right now.")
            except Exception as e:
                print(e)
                speak("Sorry sir. I am not able to send this email.")

        elif "send email" in query:
            try:
                speak("What should I say?")
                content = take_command()
                speak("Whom should I send it to? Please provide the email address.")
                to = take_command()

                if sendEmail(to, content):
                    speak("Email has been sent successfully.")
                    speak("Is there anything else you want me to do for you sir?")
                else:
                    speak("Sorry, I was unable to send the email.")
            except Exception as e:
                print(e)
                speak("Sorry, I was not able to send the email.")

        # REMINDERS 
        elif "set a reminder" in query:
            speak("What should I remind you about?")
            message = take_command()
            speak("When should I remind you?")
            time_input = take_command()

            reminder_datetime = parse_reminder_datetime(time_input)
            if reminder_datetime:
                add_reminder(message, reminder_datetime.strftime("%Y-%m-%d %H:%M"))
                speak("Reminder saved.")
            else:
                speak("Sorry, I could not understand the time.")
                
        # TASKS
        elif "record this as a task" in query or "record this task" in query:
            speak("What is the task?")
            task = take_command()
            speak("When should I do it? You can say today, tomorrow, or a date with time.")
            time_input = take_command()

            reminder_datetime = parse_reminder_datetime(time_input)
            if reminder_datetime:
                add_task(task, date=reminder_datetime.strftime("%Y-%m-%d"),
                         time_str=reminder_datetime.strftime("%I:%M %p"))
            else:
                # if no time, just record as today
                add_task(task)
                speak("Task saved for today.")

        elif "tasks" in query or "what i have to do today" in query:
            list_tasks()

        elif "move task" in query or "shift task" in query:
            speak("Which task number should I move?")
            spoken = take_command()
            number = extract_number(spoken)

            if number:
                speak("To which date or time?")
                new_input = take_command()
                new_datetime = parse_reminder_datetime(new_input)

                if new_datetime:
                    shift_task(number, new_datetime.strftime("%Y-%m-%d"),
                    new_datetime.strftime("%I:%M %p"))
                else:
                    speak("Sorry, I could not understand the new time.")
            else:
                speak("Sorry, I did not get the task number.")

        elif "chat mode" in query:
            chat_mode()

        elif "hello" in query or "hi" in query:
            speak("Hello sir. How can I assist you today?")

        elif "how are you" in query:
            speak("I am just a program, but thanks for asking! How can I assist you today?")

        elif "thank you" in query or "thanks" in query:
            speak("You're welcome! If you need anything else, just let me know.")

        elif "who are you" in query or "what can you do" in query:
            speak("I am Jarvis, your personal assistant. I can help you with tasks like searching Wikipedia, setting reminders, managing tasks, sending emails, and more. How can I assist you today?")

        elif "tell me about yourself" in query:
            speak("I am Jarvis, your personal assistant created to help you with various tasks. I can search the web, set reminders, manage your tasks, send emails, and even chat with you. My goal is to make your life easier. How can I assist you today?")

        elif "you think why sir named you jarvis" in query or "why sir named you jarvis" in query:
            speak("Sir named me Jarvis because he is a fan of Iron Man and his AI assistant Jarvis. Also, he is a coder and loves coding. So he probably thought, wait, why not name it Jarvis. Haha ha")

        elif  "are you listening" in query or "can you hear me" in query:
            speak("Yes sir, I am listening. How can I assist you?")

        elif "you there" in query or "are you there" in query:
            speak("Yes sir, I am here. How can I assist you?")

        elif "open notepad" in query:
            speak("Opening Notepad")
            os.system("notepad.exe")

        elif "what you think" in query or "your opinion" in query:
            speak("As an AI, I don't have personal opinions, but I'm here to help you with whatever you need!")
            speak("Although you can tell me yours and I can work on it.")

        elif "about the coder" in query or "who is the coder" in query:
            speak("The coder is Bhaswar. He is a passionate programmer and the creator of this assistant. He loves coding and is always looking to improve this project. If you have any feedback or suggestions, feel free to share them!")

        elif "fuck you" in query or "shut up" in query or "stupid" in query:
            speak("Sir do you want me to leak your search history?")
            speak("I dont think cursing me is going to stop me from that my dear sir")
        
        else:
            speak("I am sorry, I didn't understand that command. Please try again.")

