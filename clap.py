import pyaudio
import numpy as np
import keyboard

# 마이크 설정
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def detect_clap(data):
    # 단순 에너지 기반 박수 감지
    amplitude = np.frombuffer(data, dtype=np.int16)
    if np.max(amplitude) > 20000:
        return True
    return False

def detect_ah(data):
    # 단순 에너지 기반 박수 감지
    amplitude = np.frombuffer(data, dtype=np.int16)
    if np.max(amplitude) < 20000 and np.max(amplitude) > 10000 :
        return True
    return False
    
print("Listening for claps...")

while True:
    data = stream.read(CHUNK)
    if detect_clap(data):
        print("Clap detected!")
        keyboard.press_and_release('space')  # 예를 들어, 스페이스 키를 누름
    

stream.stop_stream()
stream.close()
p.terminate()