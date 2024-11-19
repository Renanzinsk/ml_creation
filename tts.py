import pyttsx3

def textToSpeech(take):
    text_speech = pyttsx3.init()
    text_speech.setProperty('rate', 160)  # Speed of speech (words per minute)
    text_speech.say(take)
    text_speech.runAndWait()