import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import json 
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
   engine.say(audio)
   engine.runAndWait()
   
   #This function will greet the user.
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning boss!")
        speak("I'm your AI assistant. Please tell me how may i assist you")
    elif hour>=12 and hour<18:
    
        speak("Good Afternoon boss!")
        speak("I'm your AI assistant. Please tell me how may i assist you")
    else:
        speak("Good Evening boss!")
        speak("I'm your AI assistant. Please tell me how may i assist you")
    
def takeCommand():   
     #It takes microphone input from user and returns string output.
     
     r = sr.Recognizer()
     with sr.Microphone() as source:
         print("Listening...")
        #  r.pause_threshold = 5
         r.adjust_for_ambient_noise(source)
         audio = r.listen(source)
     
     
     try:
         print("Recognizing...")
         query = r.recognize_google(audio, language='en-in')
         print(f"user said: {query}\n")
         
     except Exception as  e:
        #  print(e)
         
        print("Say that again please....")  
        return "None"
     
     return query
if __name__== "__main__":
    wishMe()
    while True:
    # if 1:
        query = takeCommand().lower()
       
        #Logic for executing tasks based on query string
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            
        elif 'open lpu' in query:
            webbrowser.open("ums.lpu.in/lpuums/")
            
        elif 'open google' in query:
            webbrowser.open("google.com")
            
        elif 'open gmail' in query:
            webbrowser.open("gmail.com")
            
        elif 'play music'  in query:
            music_dir = 'E:\\AI VOCE ASSISTANT\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
         
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"sir, the time is {strTime}")     
        
        elif 'open code' in query:
            codePath = "C:\\Users\\satya\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"  
            os.startfile(codePath)
        
        
        elif 'open edge' in query:
            edgePath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe" 
            os.startfile(edgePath)
        
        
        elif 'open chrome' in query:
            chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  
            os.startfile(chromePath)
            
        
        elif 'open excel' in query:
            excelPath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE" 
            os.startfile(excelPath)
            
        
        elif 'open powerpoint' in query:
            ppPath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE" 
            os.startfile(ppPath)
    
        elif 'open word' in query:
            wordPath = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE" 
            os.startfile(wordPath)
       
        elif 'how are you' in query:
            speak(f"I'm working smooth, anything else i can help you with?")
        
        elif 'boss' in query:
            speak(f"Mister Sahil created me. and he is my boss!")
        
        elif 'your name' in query:
            speak("Hii! my name is Sunny. how may i assist you?")
    
        elif 'close' in query:
            speak(f"Have a Good day!")
            quit()
        
        elif 'news' in query:
            webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India, Happy reading')
            
        elif 'search'  in query:
            query = query.replace("search", "")
            webbrowser.open_new_tab(query)
            
        elif "weather" in query:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response =requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")
