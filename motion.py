import cv2
import numpy as np
import keyboard

# 카메라 초기화
cap = cv2.VideoCapture(0)
fgbg = cv2.createBackgroundSubtractorMOG2()

previous_center = None
key_state = {'a': False, 'd': False}

def press_key(key):
    if not key_state.get(key, False):
        keyboard.press(key)
        key_state[key] = True

def release_key(key):
    if key_state.get(key, False):
        keyboard.release(key)
        key_state[key] = False

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    fgmask = fgbg.apply(frame)
    
    # 이진화 및 노이즈 제거
    _, thresh = cv2.threshold(fgmask, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.medianBlur(thresh, 5)
    
    # 윤곽선 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    largest_contour = None
    max_area = 0
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area and area > 300:  # 너무 작은 움직임 무시
            max_area = area
            largest_contour = contour
    
    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        current_center = (x + w // 2, y + h // 2)
        
        if previous_center is not None:
            dx = current_center[0] - previous_center[0]
            dy = current_center[1] - previous_center[1]
            
            if abs(dy) > abs(dx):  # 수직 이동이 더 큰 경우
                if dy > 0 and abs(dy) > 150:  # 아래쪽으로 크게 움직일 때만
                    keyboard.press_and_release('s')
                    print("Down")
                elif dy < 0 and abs(dy) > 150:  # 위쪽으로 크게 움직일 때만
                    keyboard.press_and_release('space')
                    print("Up")
            else:  # 수평 이동이 더 큰 경우
                if dx > 0:
                    press_key('d')
                    release_key('a')
                    release_key('w')
                    release_key('s')
                    print("Right")
                else:
                    press_key('a')
                    release_key('d')
                    release_key('w')
                    release_key('s')
                    print("Left")
        
        previous_center = current_center
    else:
        # 모든 키를 놓기
        release_key('w')
        release_key('a')
        release_key('s')
        release_key('d')
    
    # 화면에 비디오 스트림 표시
    cv2.imshow('frame', frame)
    
    # 'q' 키를 누르면 루프 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
