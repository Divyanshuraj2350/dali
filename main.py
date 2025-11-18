import google.generativeai as genai
import speech_recognition as sr
import emoji as em
import os
from gtts import gTTS
import time
from datetime import datetime
import requests
import pywhatkit
import pyautogui
import time
import subprocess
import music as spo
import sys

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

# Using gTTS for text-to-speech (free, no setup needed)
genai.configure(api_key='AIzaSyA5dhs_HcjZXxYCUyzccIaQk3ekwg05wCU')
model = genai.GenerativeModel('gemini-pro')

os.system('cls' if os.name == 'nt' else 'clear')

r = sr.Recognizer()

os.system('cls' if os.name == 'nt' else 'clear')


def read_aloud(input_text):
    """Convert text to speech using gTTS and play it"""
    try:
        tts = gTTS(text=input_text, lang='en', slow=False)
        tts.save('output.mp3')
        subprocess.run(['afplay', 'output.mp3'])
    except Exception as e:
        print(f"TTS Error: {e}")


def introduction():
    text = 'Hello, I am Dali. Your personal voice assistant.'
    current_time = datetime.now().time()
    if current_time.hour < 12:
        print("Good morning, happy soul.")
        msg = "Good morning happy soul"
        read_aloud(msg)
        time.sleep(0.5)
        print(text)
        read_aloud(text)
    elif current_time.hour < 18:
        print("Good afternoon, happy soul")
        msg1 = "Good afternoon happy soul"
        read_aloud(msg1)
        time.sleep(0.5)
        print(text)
        read_aloud(text)
    else:
        print("Good evening, happy soul")
        msg2 = "Good evening happy soul"
        read_aloud(msg2)
        time.sleep(0.5)
        print(text)
        read_aloud(text)


def generate(prompt):
    response = model.generate_content(
        ["You will generate answers within 75 tokens. Write in a continuous flow, avoiding bulleted lists." + prompt])
    print("Dali:", response.text)
    read_aloud(response.text)


def get_coordinates(city_name):
    """Get latitude and longitude for a city"""
    try:
        params = {
            'name': city_name,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        response = requests.get(GEOCODING_URL, params=params)
        data = response.json()

        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            return result['latitude'], result['longitude'], result['name'], result.get('country', '')
        else:
            return None, None, None, None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None, None, None, None


def get_weather(city_name):
    """Get current weather for a city using Open-Meteo API"""
    try:
        # Get coordinates first
        lat, lon, full_city_name, country = get_coordinates(city_name)

        if lat is None:
            return f"Sorry, I couldn't find the city '{city_name}'"

        # Get weather data
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': 'true',
            'temperature_unit': 'celsius'
        }

        response = requests.get(WEATHER_URL, params=params)
        data = response.json()

        if 'current_weather' in data:
            current = data['current_weather']
            temp = current['temperature']
            windspeed = current['windspeed']

            # Weather code interpretation
            weather_code = current['weathercode']
            weather_desc = get_weather_description(weather_code)

            return f"Weather in {full_city_name}, {country}: {weather_desc}. Temperature is {temp}°C with wind speed {windspeed} km/h"
        else:
            return "Could not fetch weather data"

    except Exception as e:
        return f"Weather error: {e}"


def get_weather_description(code):
    """Convert weather code to description"""
    weather_codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Foggy", 51: "Light drizzle", 53: "Moderate drizzle",
        55: "Dense drizzle", 61: "Slight rain", 63: "Moderate rain",
        65: "Heavy rain", 71: "Slight snow", 73: "Moderate snow",
        75: "Heavy snow", 80: "Rain showers", 81: "Moderate rain showers",
        82: "Violent rain showers", 95: "Thunderstorm", 96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, "Unknown weather")


def get_weather_description(code):
    """Convert weather code to description"""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, "Unknown weather")


def weather(city_name):
    """Wrapper function for weather - for backwards compatibility"""
    result = get_weather(city_name)
    print("Dali:", result)
    read_aloud(result)


def send_msg(msg, person):
    c = datetime.now()
    time = c.strftime('%H:%M:%S')
    hour = int(time[0:2])
    m = int(time[3:5])+1
    sec = int(time[6:8])
    if sec >= 50:
        m += 1
    if m >= 60:
        m = m % 60
        hour += 1
    if hour == 24:
        hour = 0
    sending(msg, person, hour, m)


def sending(msg, person, hour, m):
    try:

        person = '+91'+person
        pywhatkit.sendwhatmsg(person, msg, hour, m, 10)
        time.sleep(10)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.hotkey('ctrl', 'w')
        pyautogui.hotkey('ctrl', 'shift', 'w')

    except:
        error = "Error while sending msg"
        print(error)
        read_aloud(error)


def conversation_flow():
    try:
        introduction()  # Greet user first

        with sr.Microphone() as source:
            intro = "Dali is ready. You can speak now."
            print(intro)
            read_aloud(intro)

            while True:
                try:
                    print("\nListening...")
                    audio = r.listen(source, timeout=10, phrase_time_limit=10)

                    try:
                        prompt = r.recognize_google(audio)
                        print(f"You said: {prompt}")
                    except sr.UnknownValueError:
                        print("Sorry, I couldn't understand that.")
                        continue
                    except sr.RequestError as e:
                        print(f"Speech recognition error: {e}")
                        continue

                    prompt_lower = prompt.lower()

                    # Exit commands
                    if any(word in prompt_lower for word in ["quit", "bye", "shut up", "go away", "exit"]):
                        farewell = "Goodbye! Have a great day!"
                        print("Dali:", farewell)
                        read_aloud(farewell)
                        sys.exit()

                    # Capabilities
                    elif any(word in prompt_lower for word in ["capabilities", "capability", "able", "can you do"]):
                        text = "I can answer questions, show weather forecast, send WhatsApp messages, and play Spotify music."
                        print("Dali:", text)
                        read_aloud(text)

                    # Greetings (check exact phrases to avoid false matches)
                    elif prompt_lower in ["hello", "hey", "hi", "hey dali", "hello dali"] or prompt_lower.startswith("what's up"):
                          hello = "Hey there! I am Dali. I hope you have a nice day."
                          print("Dali:", hello)
                          read_aloud(hello)

                    # Time
                    elif "time" in prompt_lower:
                        current_time = datetime.now().strftime("%I:%M %p")
                        response = f"The time is {current_time}"
                        print("Dali:", response)
                        read_aloud(response)

                    # Date
                    elif "date" in prompt_lower or "today" in prompt_lower:
                        current_date = datetime.now().strftime("%B %d, %Y")
                        response = f"Today is {current_date}"
                        print("Dali:", response)
                        read_aloud(response)
                    # Weather
                    elif any(word in prompt_lower for word in ["weather", "forecast", "temperature", "sky"]):
                        # Try to extract city name from the prompt
                        city_name = None

                        # Remove weather keywords to isolate city name
                        words = prompt_lower.replace("weather", "").replace("forecast", "").replace("temperature", "").replace(
                            "tell me", "").replace("about", "").replace("in", "").replace("the", "").strip()

                        # Check if there's a city name in the original prompt
                        if words:
                            city_name = words
                            print(f"Detected city: {city_name}")
                            weather_info = get_weather(city_name)
                            print("Dali:", weather_info)
                            read_aloud(weather_info)
                        else:
                            # Ask for city if not detected
                            citytext = "Which city would you like to know about?"
                            print("Dali:", citytext)
                            read_aloud(citytext)

                            try:
                                audio = r.listen(source, timeout=5)
                                city_name = r.recognize_google(audio)
                                print(f"You said: {city_name}")

                                weather_info = get_weather(city_name)
                                print("Dali:", weather_info)
                                read_aloud(weather_info)
                            except Exception as e:
                                print(f"Weather error: {e}")
                                # Default to Delhi if no response
                                weather_info = get_weather("Delhi")
                                print("Dali:", weather_info)
                                read_aloud(weather_info)

                    # WhatsApp
                    elif "whatsapp" in prompt_lower or "message" in prompt_lower:
                        wapp = "Please make sure WhatsApp Web is logged in on your browser."
                        print("Dali:", wapp)
                        read_aloud(wapp)
                        time.sleep(2)
    
                        no = "Tell me the 10-digit phone number"
                        print("Dali:", no)
                        read_aloud(no)

                        try:
                            audio = r.listen(source, timeout=5)
                            number_text = r.recognize_google(audio)
                            print(f"You said: {number_text}")
        
                            # Extract only digits
                            number = ''.join(filter(str.isdigit, number_text))
      
                            if len(number) < 10:
                                error_msg = "I need a 10-digit phone number. Please try again."
                                print("Dali:", error_msg)               
                                read_aloud(error_msg)
                                continue
        
                            # Take last 10 digits if more than 10
                            number = number[-10:]
        
                            msg_prompt = "What message should I send?"
                            print("Dali:", msg_prompt)
                            read_aloud(msg_prompt)
        
                            audio = r.listen(source, timeout=5)
                            message = r.recognize_google(audio)
                            print(f"You said: {message}")
        
                            send_msg(message, number)
                            sent = "I have sent your message"
                            print("Dali:", sent)
                            read_aloud(sent)
                        except Exception as e:
                            print(f"WhatsApp error: {e}")
                            read_aloud("Sorry, I couldn't send the message")
                    
                    # Music
                    elif any(word in prompt_lower for word in ["music", "spotify", "song", "play"]):
                        song = "Opening Spotify. Make sure it's running on your system."
                        print("Dali:", song)
                        read_aloud(song)
                        try:
                            spo.search_play()
                        except Exception as e:
                            print(f"Music error: {e}")
                            read_aloud("Sorry, Spotify is not available right now")
                    
                    # Joke
                    elif "joke" in prompt_lower:
                        generate("Tell me a funny joke")
                    
                    # Who are you
                    elif "who" in prompt_lower:
                        response = model.generate_content(["You will generate answers within 75 tokens. " + prompt])
                        original = str(response.text)
                        new = original.replace("Gemini", "Dali").replace("developed", "powered").replace("Google", "Ananya")
                        print("Dali:", new)
                        read_aloud(new)
                    
                    # General AI conversation
                    else:
                        generate(prompt)
                
                except Exception as e:
                    print(f"Error: {e}")
                    continue
    
    except KeyboardInterrupt:
        print("\n\nGoodbye! Dali is shutting down.")
        sys.exit(0)
                        
