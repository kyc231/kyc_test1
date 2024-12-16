import cv2
import numpy as np
import vgamepad as vg
import pyaudio
import threading
import time

# 가상 게임패드 초기화
gamepad = vg.VX360Gamepad()

# 카메라 초기화
cap = cv2.VideoCapture(0)

# 빨간색 범위 설정 (HSV 색 공간)
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# 노란색 범위 설정 (HSV 색 공간)
lower_yellow = np.array([20, 100, 100])
upper_yellow = np.array([30, 255, 255])

# 오디오 스트림 초기화
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 2000  # 박수 소리 감지 임계값

def normalize(value, start, end):
    """
    값을 -32768에서 32767 사이로 정규화합니다.
    """
    return int(65535 * (value - start) / (end - start) - 32768)

def move_stick(x, y):
    gamepad.left_joystick(x_value=x, y_value=y)
    gamepad.update()

def detect_clap(data):
    # 오디오 데이터를 numpy 배열로 변환
    audio_data = np.frombuffer(data, dtype=np.int16)
    # 절대값을 취해 평균을 계산
    amplitude = np.abs(audio_data).mean()
    return amplitude > THRESHOLD

def listen_for_claps():
    # pyaudio 객체 생성
    p = pyaudio.PyAudio()

    # 오디오 스트림 열기
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("박수를 치면 패드 A가 눌립니다...")

    try:
        while True:
            # 오디오 데이터를 읽음
            data = stream.read(CHUNK, exception_on_overflow=False)
            # 박수 감지
            if detect_clap(data):
                print("박수 감지!")
                # 패드 A 누르기
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()
                time.sleep(0.1)
                # 짧은 시간 후 버튼 놓기
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
                gamepad.update()
    except KeyboardInterrupt:
        print("종료합니다...")
    finally:
        # 오디오 스트림 닫기
        stream.stop_stream()
        stream.close()
        p.terminate()

# 마지막 검출된 x 좌표와 y 좌표를 저장하는 변수
last_x = 0
last_y = 0

# 박수 감지 쓰레드 시작
#clap_thread = threading.Thread(target=listen_for_claps)
#clap_thread.daemon = True
#clap_thread.start()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 프레임을 HSV 색 공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 빨간색 범위에 해당하는 마스크 생성
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    
    # 초록색 범위에 해당하는 마스크 생성
    mask_green = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # 빨간색 마스크에 모폴로지 연산 적용 (노이즈 제거)
    mask_red = cv2.erode(mask_red, None, iterations=2)
    mask_red = cv2.dilate(mask_red, None, iterations=2)
    
    # 초록색 마스크에 모폴로지 연산 적용 (노이즈 제거)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)
    
    # 윤곽선 찾기
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours_red:
        # 가장 큰 윤곽선 선택
        largest_contour_red = max(contours_red, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour_red)
        current_center_x = x + w // 2
        
        # x 좌표를 아날로그 스틱 값으로 변환
        left_x = normalize(current_center_x, 0, frame.shape[1])
        
        # 아날로그 스틱 이동
        move_stick(left_x, last_y)
        
        # 마지막 x 좌표 업데이트
        last_x = left_x
        
        # 중심에 원 표시 (디버깅 용도)
        cv2.circle(frame, (current_center_x, y + h // 2), 5, (0, 255, 0), -1)
    else:
        # 빨간색 점이 없을 때 마지막 x 좌표로 고정
        move_stick(last_x, last_y)
    
    #if contours_green:
    #    # 초록색 점이 있으면 Y축을 조금 올림
    #    left_y = 32767 // 4  # 최대 값의 1/4 정도 올림
    #    move_stick(last_x, left_y)
    #    last_y = left_y
    #else:
    #    # 초록색 점이 없으면 Y축을 0으로 복귀
    #    move_stick(last_x, 0)
    #    last_y = 0
    
    # 화면에 비디오 스트림 표시
    cv2.imshow('frame', frame)
    
    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
