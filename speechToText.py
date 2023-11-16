import speech_recognition as sr


def speechToText():
    r = sr.Recognizer()   
    try:         
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)
            audio = r.listen(source, timeout=5)

            text = r.recognize_google(audio)
            text = text.lower()
 
            print(text)
             
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
         
    except sr.UnknownValueError:
        print("unknown error occurred")

if __name__ == "__main__":
    speechToText()