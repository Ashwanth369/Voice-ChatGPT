# import asyncio
# import speech_recognition as sr


# class VoiceRecorder:

#     def __init__(self):
#         self.recording = False
#         self.recognizer = sr.Recognizer()
#         self.microphone = sr.Microphone()
        
#     def onClick(self):
#         if self.recording:
#             self.recording = False
#         else:
#             self.recording = True
#             res = asyncio.run(self.main())
    
#     async def main(self):
#         result = await asyncio.gather(self.record(), self.user_input())
#         return result
    
#     async def speechToText(self, audio):
#         text = ""
#         try:
#             text = self.recognizer.recognize_google(audio)
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))
#         except sr.UnknownValueError:
#             print("unknown error occurred")
#         return text
    
#     async def user_input(self):
#         await asyncio.sleep(10)
#         global flag
#         flag = False
#         print("User Input:",flag)

#     async def record(self):
#         tasks = []
#         i = 0
#         with self.microphone as source:
#             self.recognizer.adjust_for_ambient_noise(source)
#             global flag
#             while flag:
#                 try:
#                     i += 1
#                     audio = await asyncio.wait_for(
#                         asyncio.to_thread(self.recognizer.listen, source, 5, 2), timeout=5
#                     )
#                     task = asyncio.create_task(self.speechToText(audio))
#                     tasks.append(task)
#                 except Exception:
#                     continue

#         results = await asyncio.gather(*tasks)
#         return " ".join(results)

import asyncio
import speech_recognition as sr
import aioconsole

recognizer = sr.Recognizer()
microphone = sr.Microphone()

flag = True

async def sleep_random(audio):
    text = ""
    try:
        text = recognizer.recognize_google(audio)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occurred")
    return text

async def f1(audio):
    text = ""
    try:
        text = recognizer.recognize_google(audio)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    except sr.UnknownValueError:
        print("unknown error occurred")
    return text

async def user_input():
    global flag
    await aioconsole.ainput("Press Enter to stop recording:")
    flag = False

async def f2():
    tasks = []
    i = 0
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        global flag
        while flag:
            try:
                i += 1
                audio = await asyncio.to_thread(recognizer.listen, source, 5, 2)
                task = asyncio.create_task(f1(audio))
                tasks.append(task)
            except Exception:
                continue

    results = await asyncio.gather(*tasks)
    return results

async def main():
    results, _ = await asyncio.gather(f2(), user_input())
    text = []
    for res in results:
        if res is not None and len(res) > 0:
            text.append(res)
    return text

res = asyncio.run(main())
print("Final Result:", " ".join([r for r in res if len(r) > 0]))