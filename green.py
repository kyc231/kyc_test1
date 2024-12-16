import cv2
import numpy as np
import keyboard

# 카메라 초기화
cap = cv2.VideoCapture(0)

# 초록색의 HSV 범위 설정
lower_green = np.array([35, 100, 100])
upper_green = np.array([85, 255, 255])

previous_center = None
key_state = {'up': False, 'down': False, 'right': False, 'left': False}

def press_key(key):
    if not key_state[key]:
        keyboard.press(key)
        key_state[key] = True

def release_key(key):
    if key_state[key]:
        keyboard.release(key)
        key_state[key] = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 프레임을 HSV 색상 공간으로 변환
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 초록색 영역 마스크 생성
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # 노이즈 제거를 위한 모폴로지 연산 적용
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 윤곽선 찾기
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(largest_contour) > 200:  # 너무 작은 물체는 무시
            x, y, w, h = cv2.boundingRect(largest_contour)
            current_center = (x + w // 2, y + h // 2)
            
            if previous_center is not None:
                dx = current_center[0] - previous_center[0]
                dy = current_center[1] - previous_center[1]
                
                if abs(dx) > abs(dy):  # 수평 이동이 더 큰 경우
                    if dx > 0:
                        press_key('right')
                        release_key('left')
                        release_key('up')
                        release_key('down')
                        print("Right")
                    else:
                        press_key('left')
                        release_key('right')
                        release_key('up')
                        release_key('down')
                        print("Left")
                else:  # 수직 이동이 더 큰 경우
                    if dy > 0:
                        press_key('down')
                        release_key('up')
                        release_key('right')
                        release_key('left')
                        print("Down")
                    else:
                        press_key('up')
                        release_key('down')
                        release_key('right')
                        release_key('left')
                        print("Up")
            
            previous_center = current_center
        else:
            # 모든 키를 놓기
            release_key('up')
            release_key('down')
            release_key('right')
            release_key('left')
    else:
        # 모든 키를 놓기
        release_key('up')
        release_key('down')
        release_key('right')
        release_key('left')
    
    # 화면에 비디오 스트림 표시
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    
    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
