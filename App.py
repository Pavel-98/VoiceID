
import os
import tkinter
from functools import partial
from multiprocessing import Process
from threading import Thread
from tkinter import *

import SearchProcess
from Recorder import input_request
from SpeechToText import recognize_speech
from voice_auth import deleteUserBiometry, delete

width = 35
height = 1


window = Tk(screenName='Система голосового пошуку')
window.title('Система голосового пошуку')
defaultLanguage = StringVar()
defaultLanguage.set('uk-UA')
languages = ['uk-UA', 'us-EN']
thread = Thread()
isThread = False
def open_file(path):
    os.startfile(path)
def compone(information, limit):
    info = str(information)
    if len(info) > limit:
        return '   '+ info[0: limit - 3] + '...'
    elif len(info) < limit:
        res = ''
        for number in range(0, limit - len(info)):
            res += ' '
        return '   ' + res + info
    return '   ' + info
def search():
    thread = Thread(target=search_thread)
    thread.daemon = True
    thread.start()

def stop():
    global isThread
    if isThread:
        searchButton['text'] = 'Пошук'
        searchButton['command'] = search_thread



def search_thread():
    global isThread
    global results
    results.destroy()
    create_results_label()
    requestText['text'] = 'Розпізнаний запит: '
    resultsWord['text'] = 'Результати: '+'\n'

    isThread = True
    searchButton['command'] = None
    try:
        input_request()
    except Exception as e:
        print(e)
        return

    request = recognize_speech('request.wav', defaultLanguage.get()).lower()#u

    if request:
        requestText['text'] += request
    else:
        resultsWord['text'] += 'Не вдалося розпізнати запит'
        stop()
        return

    searchButton['text'] = 'Проводиться пошук'
    SearchProcess.initialize_process(True, voice_search.get())
    SearchProcess.StartProcess(request.lower(), defaultLanguage.get())

    for search_result in SearchProcess.results[request]:
        '''resultLabel'''
        buttonText    = compone('Запит: '+search_result['request'], 10 + 15) + compone(' шлях: '+search_result['path'], 10 + 15) + compone(' пріорітет: '+str(search_result['priority']), 14) + compone(' позиція у тексті: '+str(search_result['coordinates']), 16+ 14) + '\n'#compone(str(search_result['coordinates']), 16) + '\n'#position'])+'\n'
        button = Button(results, text=buttonText, command=partial(open_file, search_result['path']))
        button.pack()
    stop()

updateButton = Button(text='Оновити АБД', command=SearchProcess.updateAudioBase)
updateButton.pack()
requestText = Label(window, text='Розпізнаний запит: ')
requestText.pack()
text_search = IntVar(window)
voice_search = IntVar(window)
text_check = Checkbutton(window, text='У тексті', variable=text_search)

voice_check = Checkbutton(window, text='Враховувати  біометрію голосу', variable=voice_search)
voice_check.pack()
searchButton = Button(window, text='Пошук', command=search_thread)

searchButton.pack()
languageOption = OptionMenu(window, defaultLanguage, *languages)
languageOption.pack()
resultsWord = Label(text='----------\nРезультати: '+ '\n')
resultsWord.pack()
results = Label()
def create_results_label():
    global results
    results = Label(window)
    results.pack()
create_results_label()
SearchProcess.load_data_bases()
window.mainloop()

