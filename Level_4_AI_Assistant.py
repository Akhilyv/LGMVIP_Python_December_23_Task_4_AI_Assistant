from gtts import gTTS
import speech_recognition as sr
import os
import datetime
import time
import webbrowser
import subprocess

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("start output.mp3")
    time.sleep(3)  # Pause for the duration of the speech

def get_voice_input(speaking_flag):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        if not speaking_flag:
            print("Say something...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        else:
            audio = recognizer.listen(source, timeout=3)  # Set a timeout during speaking

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        if not speaking_flag:
            print("Sorry, I didn't catch that. Can you please repeat?")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def process_question(command):
    if "hello" in command or "hi" in command:
        speak("Hi there! How can I assist you?")
    elif "your name" in command:
        speak("I'm your personal assistant.")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {current_time}")
    elif "weather" in command:
        # You can replace the location with the desired location for weather information
        weather_url = "https://www.google.com/search?q=weather"
        webbrowser.open(weather_url)
    elif "search" in command:
        query = command.replace("search", "").strip()
        google_search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(google_search_url)
    elif "open file" in command:
        try:
            subprocess.Popen(["notepad.exe"])  # Open Notepad as an example
            speak("File opened successfully.")
        except Exception as e:
            print(f"Error opening file: {e}")
            speak("Sorry, I couldn't open the file.")
    elif "quit" in command or "exit" in command:
        speak("Goodbye! Have a great day.")
        return True
    else:
        speak("Sorry, I didn't understand. Can you repeat?")
    return False

def main():
    speak("Hello! I am your voice assistant. How can I help you?")

    while True:
        command = get_voice_input(False)

        if process_question(command):
            break

if __name__ == "__main__":
    main()
