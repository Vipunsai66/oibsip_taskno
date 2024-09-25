import speech_recognition as sr
import pyttsx3
import smtplib
import requests
import spacy
import json
import os
from dotenv import load_dotenv

# Load environment variables (for storing sensitive information securely)
load_dotenv()
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize NLP model (spaCy)
nlp = spacy.load("en_core_web_sm")

# Helper function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to user input and convert speech to text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return None

# Function to send an email using SMTP
def send_email(to, subject, body):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(EMAIL_USER, to, message)
        server.quit()
        speak("Email sent successfully!")
    except Exception as e:
        speak("Failed to send the email.")
        print(f"Error: {e}")

# Function to fetch weather data using OpenWeatherMap API
def get_weather(city):
    try:
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temp = main["temp"]
            temp_celsius = temp - 273.15  # Convert from Kelvin to Celsius
            return f"Weather in {city}: {weather_desc}, Temperature: {temp_celsius:.2f}°C"
        else:
            return "City not found."
    except Exception as e:
        speak("Failed to fetch the weather data.")
        print(f"Error: {e}")
        return None

# Load custom commands from a JSON file
def load_custom_commands():
    try:
        with open('commands.json', 'r') as file:
            commands = json.load(file)
        return commands
    except FileNotFoundError:
        return {}

# Function to add new custom commands
def add_custom_command(trigger, response):
    commands = load_custom_commands()
    commands[trigger] = response
    with open('commands.json', 'w') as file:
        json.dump(commands, file)
    speak(f"Custom command '{trigger}' added.")

# Process query using Natural Language Processing (NLP)
def process_query(query):
    doc = nlp(query)
    for token in doc:
        print(token.text, token.pos_, token.dep_)

# Main function to run the voice assistant
def run_voice_assistant():
    speak("Hello! How can I assist you today?")
    while True:
        query = listen()
        if query:
            # Custom command handling
            commands = load_custom_commands()
            if query in commands:
                speak(commands[query])

            # Weather query
            elif "weather" in query:
                city = query.split("in")[-1].strip()
                weather = get_weather(city)
                if weather:
                    speak(weather)

            # Email sending
            elif "send email" in query:
                speak("To whom should I send the email?")
                recipient = listen()
                speak("What is the subject?")
                subject = listen()
                speak("What should I say?")
                body = listen()
                send_email(recipient, subject, body)

            # Custom command addition
            elif "add command" in query:
                speak("What should trigger the custom command?")
                trigger = listen()
                speak("What should I respond with?")
                response = listen()
                add_custom_command(trigger, response)

            # Exit the assistant
            elif "stop" in query or "exit" in query:
                speak("Goodbye!")
                break

            else:
                speak("Sorry, I didn't understand that command.")

# Run the voice assistant
if __name__ == "__main__":
    run_voice_assistant()
