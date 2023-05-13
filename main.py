import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import re
import datetime

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
        speak("When should I remind you? Please say the time in the format 'HH:MM' or say a number of minutes/hours")
        reminder_time = listen()
        if reminder_time:
            if ':' in reminder_time:
                try:
                    hour, minute = map(int, reminder_time.split(':'))
                    now = datetime.datetime.now()
                    reminder_datetime = datetime.datetime.combine(now.date(), datetime.time(hour, minute))
                    if reminder_datetime < now:
                        reminder_datetime += datetime.timedelta(days=1)
                    reminder_time_str = reminder_datetime.strftime("%H:%M:%S")
                    reminder_date_str = reminder_datetime.strftime("%Y/%m/%d")
                    reminder_cmd = f'schtasks /create /tn "reminder" /tr "cmd /c echo Reminder: {reminder_text} &amp;&amp; exit" /sc once /st {reminder_time_str} /sd {reminder_date_str}'
                    os.system(reminder_cmd)
                    speak("Reminder created.")
                except Exception as e:
                    print(e)
                    speak("Sorry, I could not create the reminder.")
            else:
                try:
                    match = re.search(r'(\d+)\s+(minute|hour)', reminder_time)
                    if match:
                        num = int(match.group(1))
                        units = match.group(2)
                        if units == 'minute':
                            delta = datetime.timedelta(minutes=num)
                        else:
                            delta = datetime.timedelta(hours=num)
                        reminder_datetime = datetime.datetime.now() + delta
                        reminder_time_str = reminder_datetime.strftime("%H:%M:%S")
                        reminder_date_str = reminder_datetime.strftime("%d/%m/%Y")
                        reminder_cmd = f'schtasks /create /tn "reminder" /tr "cmd /c echo Reminder: {reminder_text} &amp;&amp; exit" /sc once /st {reminder_time_str} /sd {reminder_date_str}'
                        os.system(reminder_cmd)
                        speak("Reminder created.")
                    else:
                        speak("Sorry, I did not understand the reminder time.")
                except Exception as e:
                    print(e)
                    speak("Sorry, I could not create the reminder.")

# def create_reminder(text, delay):
#     delay_seconds = 0
#     if "minute" in delay:
#         delay_seconds = int(delay.split()[0]) * 60
#     elif "hour" in delay:
#         delay_seconds = int(delay.split()[0]) * 60 * 60

#     now = datetime.datetime.now()
#     reminder_time = now + datetime.timedelta(seconds=delay_seconds)

#     with open("reminder.txt", "w") as f:
#         f.write(text)

#     reminder_cmd = f'notepad.exe "{os.getcwd()}\\reminder.txt"'

#     os.system(f'schtasks /create /tn "reminder" /tr "{reminder_cmd}" /sc once /st {reminder_time.strftime("%H:%M")}')
#     print(f"Reminder set for {reminder_time.strftime('%H:%M %p')}.")

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
    elif "exit" in text or "bye" in text:
        speak("Goodbye!")
        break
    else:
        speak("Sorry, I didn't understand that.")
