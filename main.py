#import dependencies
import pyaudio
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

#import functions
from voice import *
from shopping import *
from expense import *
from mails import *

def speak(text):
    tts = gTTS(text=text, lang="en",slow=False,tld="com.au")
    temp_file = "temp.mp3"
    tts.save(temp_file)
    audio = AudioSegment.from_file(temp_file, format="mp3")
    play(audio)
    os.remove(temp_file)

def listen():
    #delete this
    #text = "i want the tasks in recent emails"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            speak("You said: " + text)       
            return text.lower()
        except sr.UnknownValueError:
            speak("Sorry, I could not understand your speech.Try again")
            listen()
        except sr.RequestError as e:
            speak(f"Sorry, an error occurred: {e}.Try again")
            listen()
    


#driver
speak("Your personal voice assistant is active and ready to receive commands")
a = listen()
while "power down" not in a:
    if "voice note" in a:
        #TODO enter voice notes in a loop
        if "create" in a:
            speak("Moving to create a voice note")
            speak("Enter note name")
            filename = listen().replace(" ","")
            speak("Enter content")
            content = listen()

            if noting(filename,content)==1:
                speak("note created")
            else:
                speak("an error occured while creating the file")

        elif "delete" in a:
            speak("Moving to delete a voice note")
            speak("Enter note name")
            filename = listen().replace(" ","")
            if delete(filename)==1:
                speak("file successfully deleted")
            elif delete(filename)==2:
                speak("sorry but that file does not exist")
            else:
                speak("an error occrred while deleting the file")
        

        elif "recite" in a:
            speak("Moving to recite a voice note")
            speak("Enter note name")
            filename = listen().replace(" ","")
            print(filename)
            if read_out(filename)==2:
                speak("sorry but that file does not exist")
            elif read_out(filename)==0:
                speak("an error occured while reciting this file")
            else:
                speak(f"contents of {filename} are as follows")
                speak(read_out(filename))
        else:
            speak("no such function")
        #TODO add a function to edit created voice notes
        speak("anything else?")
        a = listen()

    elif "reminder" in a:
        speak("moving to create a reminder")

    elif "shopping list" in a:
        if "add" in a:
            speak("Moving to add to a list")
            speak("Enter items to add")
            #add like 10 of eggs
            flag=1
            count=0
            while(flag==1):
                entry = listen()
                print(entry)
                if "exit list" in entry:
                    speak(f"exiting list. added {count} items")
                    flag=0
                else:
                    if "of" in entry:
                        item = entry.split(" of ")
                    elif "off" in entry:
                        item = entry.split(" off ")
                    if adding(item[0],item[1])==1:
                        count+=1
                        speak("next item")
                    else:
                        speak("there was an error while adding the item")

                    
        elif "delete" in a:
            speak("Moving to delete list items")
            speak("Enter items to delete")
            flag=1
            count=0
            while(flag==1):
                #listen here
                #just enter name of item to delete
                entry = listen()
                if "exit list" in entry:
                    speak(f"exiting list after removing {count} items")
                    flag=0
                else:
                    if deleting(entry)==1:
                        count+=1
                        speak("next item")
                    elif deleting(entry)==2:
                        speak("list is empty")
                        speak(f"exiting list after removing {count} items")
                        flag=0
                    else:
                        speak("there was an error while removing the item")
                
        elif "edit" in a:
            speak("Moving to edit a list item")
            speak("enter item to edit")
            entry1 = listen()
            speak("enter new quantity")
            entry2 = listen()
            if editing(entry1,entry2)==1:
                speak("edited item successfully")
            else:
                speak("there was an error in editing the list")
        
        elif "recite" in a:
            speak("moving to recite the shopping list")
            items = recite()
            if items==2:
                speak("sorry but the list is empty")
            elif items==0:
                speak("there was an error while reciting the list")
            else:
                for item in items:
                    speak(item)
                speak("thats all")
        elif "clear" in a:
            speak("moving to clear the list")
            if clearing()==1:
                speak("list has been cleared")
            else:
                speak("there was an error while clearing the list")
        else:
            speak("no such function")
        speak("anything else")
        a = listen()
            
    elif "expense" in a:
        if "add" in a:
            speak("Moving on to add an expense")
            speak("enter data")
            flag = 1
            count = 0
            while flag==1:
                #listen here
                #"july 10 600 category1"
                entry = listen()
                if "stop track" in entry:
                    speak("ending tracker")
                    speak(f"{count} expenses added")
                    flag = 0
                else:
                    data = entry.split(" ")
                    if add_expense(data)==1:
                        count+=1
                        speak("next item")
                    else:
                        speak("there was an error in adding the expense")
        
        elif "delete" in a:
            speak("moving to delete an expense")
            speak("enter data to delete")
            flag = 1
            count = 0
            while flag==1:
                #listen here
                #july 10 category5
                data = listen()
                print(data)
                if "stop track" in data:
                    speak("ending tracker")
                    speak(f"{count} expenses deleted")
                    flag=0
                else:
                    if delete_expense(data)==2:
                        speak("sorry there are no expenses")
                        flag = 0
                    elif delete_expense(data)==1:
                        count+=1
                        speak("next item")
                    elif delete_expense(data)==3:
                        speak("expense does not exist")
                        speak("next item")
                    else:
                        speak("there was an error in deleting the expense")
        
        elif "monthly" in a:
            speak("moving to calculate monthly expense")
            flag = 1
            while flag==1:
                speak("please select a month")
                #listen here
                #just enter month name
                entry = listen()
                if "stop track" in entry:
                    speak("ending tracker")
                    flag=0
                else:
                    data = monthly_expense(entry)
                    speak(f"in {entry} you spent")
                    for i in data:
                        speak(f"{i[1]} on {i[0]}")
                    speak("thats it")
        elif "daily" in a:
            speak("moving to calculate daily expenses")
            flag = 1
            while flag==1:
                speak("please select a month")
                #listen here
                entry = listen()
                if "stop track" in entry:
                    speak("ending tracker")
                    flag = 0
                else:
                    data = daily_expense(entry)
                    speak(f"here are the daily expenses of {entry}")
                    for i in data:
                        day = i[0]
                        speak(f"on {day} you spent")
                        for j in i[1]:
                            item = j
                            amt = i[1][j]
                            speak(f"{amt} on {item}")
                    speak("thats it")
        else:
            speak("no such function")
        speak("anything else")
        a = listen()

    elif "email" in a:
        if "compose" in a:
            speak("moving to compose an email")
            speak("enter the name of the receiver")
            #listen here
            #send it to peter
            receiver = listen()
            receiver = receiver.split(" to ")[-1]
            speak("enter the subject of the mail")
            subject = listen()
            speak("what would the mail be about?")
            body = listen()
            speak("composing the mail now, please hold on")

            sent_mail = mailer(receiver,subject,body)
            #TODO check if sender in contacts before sending mail
            if sent_mail==2:
                speak("sorry the recepient is not in your contacts")
            elif sent_mail==0:
                speak("there was an error in sending the mail")
            else:
                speak("mail sent successfully. preparing to read out the mail now")
                speak(sent_mail)
                speak("end of mail")

        elif "summary" in a:
            speak("moving to summarize recently received emails")
            speak("how many emails would you like to read")
            #listen here
            num = listen().split(" last ")[-1]
            speak(f"summarizing the {num} most recent mails. this may take a while")
            summed = reader(num,1)
            if summed ==0:
                speak("sorry there was an error in summarizing the mail")
            elif summed:
                speak("here are the summarized mails")
                count = 1
                for i in summed:
                    speak(f"mail {count}")
                    speak(f"on {i[0]}, {i[1]} wrote {i[2]}")
                    count+=1
                speak("thats all")

        elif "task" in a:
            speak("moving to list out tasks from emails")
            speak("how many emails would you like to scan for tasks")
            #listen here
            num = listen().split(" last ")[-1]
            speak(f"looking for given tasks from the {num} most recent mails. this may take a while")
            tasked = reader(num,2)
            if tasked ==0:
                speak("sorry there was an error in creating the task list")
            elif tasked:
                speak("here are the tasks ive found")
                count=1
                for i in tasked:
                    speak(f"mail {count}")
                    speak(i[0])
                    count+=1
                speak("thats all")

        else:
            speak("no such function")
        speak("anything else")
        a = listen()

    else:
        speak("No command recognized. Ready to receive again.")
        a = listen()

speak("Powering down. See you later")

