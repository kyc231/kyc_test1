import sounddevice as sd
import queue
import vosk
import json

# Vosk 모델 다운로드 및 경로 설정 필요
# vosk-model-small-ko-0.22 모델을 사용하는 예제
# 모델 다운로드: https://alphacephei.com/vosk/models
model_path = "C:\\_S\\v"

# 큐 설정
q = queue.Queue()

# Vosk 모델 로드
model = vosk.Model(model_path)

# 오디오 스트림 콜백 함수
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# 마이크 스트림 설정
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("마이크를 통해 '아!'라고 외쳐보세요...")
    
    rec = vosk.KaldiRecognizer(model, 16000)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result_dict = json.loads(result)
            text = result_dict.get("text", "")
            print(f"인식된 내용: {text}")
            if "아" in text:
                print("Ah")
                break
