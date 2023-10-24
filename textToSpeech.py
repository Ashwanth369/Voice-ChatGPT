from gtts import gTTS
from io import BytesIO
import pygame
import time


def wait():
    while pygame.mixer.get_busy():
        time.sleep(1)

def speak(text, language='en'):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang=language)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    sound = pygame.mixer.Sound(mp3_fp)
    sound.play()
    wait()

if __name__ == '__main__':
	pygame.init()
	pygame.mixer.init()
	speak("Hello World!")