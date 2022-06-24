#!/bin/python3
import subprocess
import speech_recognition as sr
import weathercom
import json
import lxml
import requests
from googletrans import Translator
import wikipedia
import urllib.request
import logging
from gtts import gTTS
import pygame
from random import seed
from random import randint
import RPi.GPIO as g
import smtplib

ledpin= 12


'This method is to record the voice from microphone and save into an audio file'
def record():
	g.setmode(g.BOARD)
	g.setup(ledpin, g.OUT)
	g.output(ledpin, g.HIGH)
	print('say anything sir')
	command = 'arecord -d 3 --device=hw:2,0 --format S16_LE --rate 44100 -c1 ./speech.wav  '
	processe =subprocess.Popen(command.split() , stdout=subprocess.PIPE)
	output,error= processe.communicate()
	print (output)
	g.setup(ledpin, g.LOW)
'----------------------------------------------------------------------------------------------------------------------------------------------------$'


'This method is to convert the recorded audio file to a .txt file'
def speech_to_text():
	r = sr.Recognizer()
	with sr.AudioFile('./speech.wav') as source:
		audio_data= r.record(source)
		try :
			text = r.recognize_google(audio_data)
			print (text)
		except:
			text= 'did not hear you'
	file = open('./speech_text', 'w')
	file.write(text)
'----------------------------------------------------------------------------------------------------------------------------------------------------$'


'This method is to gather weather information for a given city'
def whetherReport(city):
    try:
    	weatherDetails = weathercom.getCityWeatherDetails(city)
    	humidity =json.loads(weatherDetails)["vt1observation"]["humidity"]
    	temp = json.loads(weatherDetails)["vt1observation"]["temperature"]
    	phrase = json.loads(weatherDetails)["vt1observation"]["phrase"]
    	file = open('./weather', 'w')
    	t = 'here is the weather report for ' +str(city)
    	h = 'humidity is '+str(humidity)
    	te = ' and the temperator is ' +str(temp)
    	p = ' and the phrases said that it is ' +str(phrase)
    	file.write(str(t)+'\n')
    	file.write(str(h)+'\n')
    	file.write(str(te)+'\n')
    	file.write(str(p)+'\n')
    except:
        file= open('./weatehr','w')
        file.write('sorry, i don\'t find your city')
'----------------------------------------------------------------------------------------------------------------------------------------------------$'


'This method is to goolge some data'
def google_search(search_data):
	result = ''
	if "who is" in search_data or "who are" in search_data:
		search_data = search_data.split(" ")[2:]
		search_data = " ".join(search_data)
		try:
			result = wikipedia.summary(search_data, sentences=2)
		except:
			result = 'I did not know him'
	print (result)
	file = open('./google_search_txt', 'w')
	file.write(result)
'----------------------------------------------------------------------------------------------------------------------------------------------------$'


"This method is to return date and time corresponding to your ip address's location "
def time_month():
    timeData = urllib.request.urlopen("http://worldtimeapi.org/api/ip").read()
    datetime = json.loads(timeData)["datetime"]
    date = datetime.split("T")[0]
    time = datetime.split("T")[1]
    hour1 = time.split(':')[0]
    minute= time.split(':')[1]
    if int(hour1) > 12:
       hour2 = int(hour1) -12
       hour3= str(hour2)+ ' PM '
    elif int(hour1)== 0:
       hour3= 'midnight'
    elif int(hour1)==12:
       hour3= '12 o\'clock'
    else:
      hour3=str(hour1)+' AM '
    text= 'time is '+ hour3 +'and '+ str(minute)+' minutes'
    file = open('./date_and_time.txt', 'w')
    file.write(text)
'----------------------------------------------------------------------------------------------------------------------------------------------------$'


'This method is to convert text to an audio file'
def text_to_audio(text):
    audio_generated  = "./output.mp3"
    mp3_response= gTTS(text=text , lang='en-us')
    mp3_response.save(audio_generated)
    pygame.mixer.init()
    pygame.mixer.music.load(audio_generated)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
'----------------------------------------------------------------------------------------------------------------------------------------------------------------------'

'This method is to send messages'
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    # Enable low security in gmail
    server.login('aissadocteur47', 'aissa832002')
    server.sendmail('aissadocteur47', to, content)
    server.close()
'----------------------------------------------------------------------------------------------------------------------------------------------------'
'Begining of the program, an infinite loop that keeps recording till a wake-word is detected, we enter the second loop, it keeps recording then processing the recorded audio, then returning with a response, if sleep-word heated the second loop ends'

text_to_audio('turn on')
while True:
    record()
    speech_to_text()
    file = open('./speech_text', 'r')
    text= file.read()
    print (text)
    list0=['alexa', 'alex', 'Alexa', 'Alex']
    for i in list0:
        if i in text:
            text_to_audio('how i can help you')
            while text != 'goodbye':
                record()
                speech_to_text()
                file = open('./speech_text', 'r')
                text= file.read()
                if 'weather' in text.lower():
                    text_to_audio('in wich city')
                    record()
                    speech_to_text()
                    file = open('speech_text', 'r')
                    city = file.read()
                    whetherReport(city)
                    file= open ('weather', 'r')
                    text= file.read()
                    text_to_audio(text)
                elif 'who are you' in text.lower():
                    text_to_audio('i am an AI voice assistant developed by mister abdelaziz aissa and mister babouasmail rostom in twothousand twenty two in algeria ')
                elif 'what is your name' in text.lower():
                    text_to_audio('my name is alexa')
                elif 'goodbye' in text.lower():
                    text_to_audio('see you again')
                elif 'are you there' in text:
                    text_to_audio('yes i\'m here')
                elif 'play music' in text.lower():
                    for _ in range(7):
                        value = randint(1,7 )
                    print(value)
                    music= "./Music/"+str(value)+".mp3"
                    pygame.mixer.init()
                    pygame.mixer.music.load(music)
                    pygame.mixer.music.play()
                elif 'stop' in text:
                    speak("What should I say?")
                    record()
                    speech_to_text()
                    file = open('speech_text', 'r')
                    content = file.read()
                    speak("whome should i send")
                    record()
                    speech_to_text()
                    file = open('speech_text', 'r')
                    to = file.read()
                    sendEmail(to, content)
                    ("Email has been sent !")
                elif 'joke' in text.lower():
                    for _ in range(2):
                        value = randint(0,1 )
                    print(value)
                    list_joke=["What did the 0 say to the 8 Nice belt","A man tells his doctor, Doctor, help me. I’m addicted to Twitter The doctor replies, Sorry, I do not follow you"]
                    joke = list_joke[value]
                    text_to_audio(joke)
                elif 'who is' in text.lower() :
                    search_data= text
                    google_search(search_data)
                    file = open('google_search_txt', 'r')
                    text= file.read()
                    text_to_audio(text)
                elif 'what can you do' in text:
                        text= 'i can tell you a joke, play music, tell you time, tell you weather etc ...'
                        text_to_audio(text)
                list=['what time is it', 'time ' , 'what is time']
                for i in list:
                    if i in text:
                        time_month()
                        file= open('date_and_time.txt','r')
                        text=file.read()
                        text_to_audio(text)
                        print (text)
                        break
        else :
            continue
