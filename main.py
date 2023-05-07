import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()

# Function to speak the given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for user's voice command and return the recognized text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
    except sr.RequestError as e:
        speak("Sorry, my speech service is down.")
        print(f"Speech service error: {e}")

# Function to create a reminder
def create_reminder():
    speak("What should I remind you about?")
    reminder_text = listen()
    if reminder_text:
        speak("When should I remind you?")
        reminder_time = listen()
        if reminder_time:
            try:
                datetime_obj = datetime.datetime.strptime(reminder_time, "%H:%M:%S")
                now = datetime.datetime.now()
                delta = datetime_obj - now.time()
                seconds = delta.seconds
                os.system(f'sleep {seconds} && say "Reminder: {reminder_text}" &')
                speak(f"Okay, I will remind you about {reminder_text} in {delta.seconds // 60} minutes.")
            except ValueError:
                speak("Sorry, I didn't understand the time format.")

# Function to create a to-do list
def create_todo_list():
    speak("What should I add to your to-do list?")
    todo_item = listen()
    if todo_item:
        with open("todo.txt", "a") as f:
            f.write(f"- {todo_item}\n")
        speak(f"Okay, I added {todo_item} to your to-do list.")

# Function to read the to-do list
def read_todo_list():
    with open("todo.txt", "r") as f:
        todo_items = f.read()
    speak("Here is your to-do list:")
    speak(todo_items)

# Function to search the web
def search_web(query):
    speak(f"Searching the web for {query}")
    url = f"https://www.duckduckgo.com/?q={query}&atb=v341-1&ia=web"
    webbrowser.open(url)

# Main loop
while True:
    speak("How can I help you?")
    text = listen()

    if not text:
        continue

    if "reminder" in text:
        create_reminder()
    elif "to-do list" in text:
        create_todo_list()
    elif "read my to-do list" in text:
        read_todo_list()
    elif "search for" in text:
        query = text.split("search for")[1].strip()
        search_web(query)
    elif "exit" in text or "stop" in text:
        speak("Goodbye!")
        break
    else:
        speak("Sorry, I didn't understand that.")
