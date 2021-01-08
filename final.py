# -*- coding: utf-8 -*-
"""
Created on Wed May  6 21:25:36 2020

@author: user
"""
from nltk.chat.util import Chat , reflections
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyttsx3 as vc
from tkinter import *
import speech_recognition as s
import threading
from googletrans import Translator


translator = Translator()  #creating instance of translator

#creating instance for text to speech
engine=vc.init()


rate = engine.getProperty('rate')   # getting details of current speaking rate
#print(rate)                        #printing current voice rate
engine.setProperty('rate', 170)


voices=engine.getProperty('voices')
#print(voices)

engine.setProperty("voice",voices[1].id)

def speak(word):
    engine.say(word)
    engine.runAndWait()




bot = ChatBot(
    'kuku',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        
        "chatterbot.logic.BestMatch"
    ],
    database='./db.sqlite3'
)

trainer = ListTrainer(bot)
data = open('./Chat_bot.txt').read()
talk = data.strip().split('\n')
trainer.train(talk)


pairs= [
        ['(hi|hello|hola|holla|Hi |Hello)',['Hey there  ',' hello dude ! ',' glad to see you again friend']],
        ["my name is (.*)",[' hii  %1 , Nice to meet you ! ']],
        ["my self (.*)",[' hii  %1 , Nice to meet you ! ']],
        ['(.*) your name',['My name is KUKU !  I am created by Oishik . ']],
        ['(.*)which city you live|where are you live',['ha ha ! Ironically I live in your PC ']],
        ['(.*) created you',['oishik created  me using NLTK !']],
        ['(.*) your creater',['oishik created  me using NLTK !']],
        ['(.*)How are you',['I am fine these days . tell about you ?']],
        ['(.*)fine',['glad to hear that ! stay safe these days !!']],
        ['(.*)Not so good(.*)',["sorry to hear that ! if anything wrong ?  You can tell me , i can help you "]],
        ['nothing(.*)',["If you don't want to tell me then it's fine . but i seriously i want to help you !! "]],
        ["(.*)are you a doctor",["no I'm not a doctor but as a friend of you i try my best to help you  "]],
        #['(.*)thank you (.*)but leave it(.*)|(.*)no nothing (.*)leave it(.*)|leave it(.*)|',["ok ! it's your choise !"]],
        ['(.*)ok(.*)',['OK !! no problem']],
        ['(.*)thank you(.*)|(.*)thanks(.*)',['You are most welcome ']],
        ['(.*)do love me|I love you',[" Sorry ! i am not interested on you ! don't mind  !"]],
        #
        #
        ['(.*) (.*)is fun ?', ['Yes !! %2 is indeed fun !','No ! i think %2 is not quite fun ! ']],
        ["(.*)ok(.*) ",["i think you don't like my answer or you hesitate "]],
        #
        #
        ['HOW THE WEATHER IN (.*)?',[' the weather in %1 is amazing like always ']],
        ['(.*)help(.*)',['i can help you plese tell me what you want !']],
        ['bye(.*)',['bye ! Take care ! ']],
        ['Good Morning(.*)',['Good Morning !  Have a great day ']],
        ['Good Night(.*)|gd n8',['Good Night !  Sweet Dreams ']]
        ]

# if we put (.*) followed by one space then which i input in the place of (.*) it will give output as it is in the place of %1
#and we can use (.*) with out no space  with the pevious or after at any word to insert anything at the input

reflections

chat = Chat(pairs,reflections)

#creating file to ask answer from bot and return the bot's answer
def ans(st):
        y=chat.respond(st)
        if y != None :
            return y
        else:
            x=bot.get_response(st)
            return x
        
#creating GUI
main = Tk()
main.geometry("500x650")
main.title("My Bot")

# add image into the GUI as label 

img = PhotoImage(file="./pic_lable.png")
photoL = Label(main, image=img)
photoL.pack(pady=20)


# take_quary : it takes audio as input from user and converts it to string and then ask from bot for response

def take_quary():
    sr=s.Recognizer()
    sr.pause_threshold=.5
    with s.Microphone() as m:
        #print('Kuku is listing . try to speak !')
        audio = sr.listen(m)
        try:
            quary = sr.recognize_google(audio, language='eng-uk')
            textF.delete(0, END)
            textF.insert(0, quary)
            ask_from_bot()
        except :
            pass
            #print("Could not recognized your voice ! try to speak again !")


# function for ask from bot for response

def ask_from_bot():
    question_before = textF.get()
    question_after = translator.translate(question_before, dest='en')
    language = question_after.src
    answer_from_bot = ans(question_after.text)
    answer_from_bot = str(answer_from_bot)
    if language != 'en':
        msgs.insert(END, "YOU :    " + question_before +' (  ' + question_after.text + '   ) ')
        answer_translate = translator.translate(answer_from_bot, dest=language)
        msgs.insert(END, "KUKU :    " + answer_translate.text + ' (   ' + answer_from_bot + '   ) ')
        speak(answer_from_bot)
    # print(type(answer_from_bot))
    else:
        msgs.insert(END, "YOU :  " + question_before)
        #print(type(answer_from_bot))
        msgs.insert(END, "KUKU :  " + str(answer_from_bot))
        speak(answer_from_bot)

    textF.delete(0, END)
    msgs.yview(END)



# create message field
frame = Frame(main)
sc = Scrollbar(frame)
msgs = Listbox(frame, width=80, height=20,yscrollcommand=sc.set)
sc.pack(side=RIGHT, fill=Y)
msgs.pack(side=LEFT, fill=BOTH, pady=1)
frame.pack()

# creating text field

textF = Entry(main, font=("Forte ", 15))
textF.pack(fill=X, pady=20)

# creating button field
btn = Button(main, text='Ask From KUKU', font=("Arial Black", 10), command=ask_from_bot)
btn.pack()

#creating a function to input by enter key

def enter_function(event):
    btn.invoke()

# going to bind main window with enter key 
main.bind('<Return>',enter_function)

# code for take audio input repeatedly from GUI
def repeat_L():
    while True:
        take_quary()      

t=threading.Thread(target=repeat_L)
t.start()


main.mainloop()

