import pyttsx3
#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

def textToSpeech(text):
    engine = pyttsx3.init()
    engine.say(text) 
    engine.runAndWait()

if __name__ == '__main__':
    textToSpeech("Hello World!")