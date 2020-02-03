from gtts import gTTS
import speech_recognition as sr
import os
import re
import webbrowser
import smtplib
import requests
import pyttsx3
#write here weather command


#voice controler code

engine = pyttsx3.init() #object creation

"""RATE"""
rate = engine.getProperty('rate') #getting details of current speaking rate
                                  #printing current voice rate
engine.setProperty('rate',90)    #setting up new voice rate

"""VOLUME"""
volume = engine.getProperty('volume') #getting to know current volume level(min=0 and max=1)
                                      #printing current volume level
engine.setProperty('volume',1.0)        #setting up volume level between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')  #getting details of current voice
engine.setProperty('voice', voices[0].id) #changing index, changes voices.1 for female

engine.say("Hello user how may I assist you")
print("Hello user how may I assist you")
engine.runAndWait()
engine.stop()


def talkToMe(audio):
    "speaks audio passed as argument"

    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

    #  use the system's inbuilt say command instead of mpg123
    #  text_to_speech = gTTS(text=audio, lang='en')
    #  text_to_speech.save('audio.mp3')
    #  os.system('mpg123 audio.mp3')


def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        engine.say('you said' + command + '\n')
        print('You said: ' + command + '\n')
        engine.runAndWait()
        engine.stop()

    #loop back to continue to listen for commands if unrecognizable speech is received
    except sr.UnknownValueError:
        engine.say("Your last command couldn't be heard")
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command


def assistant(command):
    "if statements for executing commands"

    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        engine.say("Done!")
        print('Done!')
        engine.runAndWait()
        engine.stop()

    elif 'open facebook' in command:
        reg_ex = re.search('open facebook(.*)', command)
        url = 'https://facebook.com/'
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain
            webbrowser.open(url)
            engine.say('Done!')
            print('Done!')
            engine.runAndWait()
            engine.stop()
        else:
            pass

    elif 'open youtube' in command:
        reg_ex = re.search('open youtube (.*)', command)
        url = 'https://www.youtube.com/'
        webbrowser.open(url)
        engine.say("Done!")
        print('done!')
        engine.runAndWait()
        engine.stop()

    elif 'open calculator' in command:
        reg_ex = re.search('open calculator (.*)', command)
        url = 'https://www.google.com/search?client=firefox-b-d&sxsrf=ACYBGNS-342fFwUg1NYIdYkOoKW5nyuwHw%3A1580315899456&ei=-7QxXvS9G6bDz7sP9YOWgAw&q=calculator&oq=calcalutor&gs_l=psy-ab.3...0.0..25146...0.0..0.0.0.......0......gws-wiz.CVHnRxNPCXg&ved=0ahUKEwi0p8e-n6nnAhWm4XMBHfWBBcAQ4dUDCAo&uact=5'
        webbrowser.open(url)
        engine.say("Done!")
        print('Done!')
        engine.runAndWait()
        engine.stop()

    elif 'show me trending images on web' in command:
        reg_ex = re.search('show me trending images on web (.*)', command)
        url = 'https://www.bing.com/images/trending?form=HDRSC2'
        webbrowser.open(url)
        engine.say("Done!")
        print('Done!')
        engine.runAndWait()
        engine.stop()

    elif 'what\'s the news' in command:
        reg_ex = re.search('what\'s the news (.*)', command)
        url = 'https://www.msn.com/en-in/news/world'
        webbrowser.open(url)
        engine.say("Done!")
        print('Done!')
        engine.runAndWait()
        engine.stop()

    elif'i am hungry' in command:              #show me hotels near by, where am i, hosipatal near by
        reg_ex = re.search('I am hungry (.*)', command)
        try:
            from googlesearch import search
        except ImportError:
            print("NO MODULE NAMED 'GOOGLE' FOUND")
            
        #to search
        query = "Show restaurant near me"
        url = query
        webbrowser.open_new(url)
    

        for j in search(query, tld="co.in", num=10, stop=1, pause=2):
            print(j)


    

   
    elif 'play music' in command:   #solve this
        reg_ex = re.search('play music a(.*)', command)
        file = r"C:\Users\karam\Desktop\musica.mp3"
        os.system("C:\Program Files (x86)\Windows Media Player\wmplayer.exe" + file)
        

    
   

        
        
    

    elif 'what\'s up' in command:
        talkToMe('Just doing my thing')

    
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            condition = location.condition()
            talkToMe('The Current weather in %s is %s The tempeture is %.1f degree' % (city, condition.text(), (int(condition.temp())-32)/1.8))

    elif 'weather forecast in' in command:
        reg_ex = re.search('weather forecast in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            weather = Weather()
            location = weather.lookup_by_location(city)
            forecasts = location.forecast()
            for i in range(0,3):
                talkToMe('On %s will it %s. The maximum temperture will be %.1f degree.'
                         'The lowest temperature will be %.1f degrees.' % (forecasts[i].date(), forecasts[i].text(), (int(forecasts[i].high())-32)/1.8, (int(forecasts[i].low())-32)/1.8))


    elif 'email' in command:
        talkToMe('Who is the recipient?')
        recipient = myCommand()

        if 'John' in recipient:
            talkToMe('What should I say?')
            content = myCommand()

            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)

            #identify to server
            mail.ehlo()

            #encrypt session
            mail.starttls()

            #login
            mail.login('username', 'password')

            #send message
            mail.sendmail('John Fisher', 'JARVIS2.0@protonmail.com', content)

            #end mail connection
            mail.close()

            talkToMe('Email sent.')

        else:
            talkToMe('I don\'t know what you mean!')


talkToMe('I am ready for your command')
engine.say("I am ready for your command")
engine.runAndWait()
engine.stop()

#loop to continue executing multiple commands
while True:
    assistant(myCommand())
