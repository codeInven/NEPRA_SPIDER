import speech_recognition as sr
import os
import threading
cmd="\"C:/Program Files (x86)/Notepad++/notepad++.exe\""
kcmd="taskkill /F /IM \"notepad++.exe\" /T"
r = sr.Recognizer()
with sr.Microphone() as source:                # use the default microphone as the audio source
    audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

try:
    text=r.recognize(audio)
    print("You said " + text)    # recognize speech using Google Speech Recognition
    sub_index = text.find('notpad')
    print(sub_index)
    if(sub_index>0):
        x = threading.Thread(target=os.system(cmd), args=(1,))
        x.start()
    sub_index = text.find('close')
    if(sub_index>0):
        os.system(kcmd)
    
except LookupError:                            # speech is unintelligible
    print("Could not understand audio")