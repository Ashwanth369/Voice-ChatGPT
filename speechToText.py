import threading
import speech_recognition as sr
import time

recognizer = sr.Recognizer()
microphone = sr.Microphone()

flag = True

def f1(audio):
    text = ""
    try:
        text = recognizer.recognize_google(audio)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occurred")
    return text

def user_input():
    global flag
    time.sleep(5)
    flag = False

def f2():
    tasks = []
    i = 0
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)

        global flag
        while flag:
            try:
                i += 1
                audio = recognizer.listen(source, 5, 2)
                task = threading.Thread(target=f1, args=(audio,), daemon=True)
                tasks.append(task)
                task.start()
            except Exception:
                continue

    for task in tasks:
        task.join()

    results = [task.result for task in tasks if hasattr(task, 'result')]
    return results

def main():
    results, _ = f2(), user_input()
    text = []
    for res in results:
        if res is not None and len(res) > 0:
            text.append(res)
    return text

res = main()
print("Final Result:", " ".join([r for r in res if len(r) > 0]))
