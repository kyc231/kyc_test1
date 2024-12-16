import pyautogui
import time

def automate_actions():
    while True:
        # W 키 누르기
        pyautogui.keyDown('w')
        
        # 0.3초 대기
        time.sleep(0.3)
        
        # 스페이스바 누르기
        pyautogui.press('space')
        
        # 마우스 현재 위치 저장
        current_mouse_x, current_mouse_y = pyautogui.position()
        
        # 마우스를 150픽셀 오른쪽으로 이동
        pyautogui.moveTo(current_mouse_x + 150, current_mouse_y)
        
        # 원래 위치로 돌아오기
        pyautogui.moveTo(current_mouse_x, current_mouse_y)
        
        # W 키를 떼지 않고 다음 루프로 계속하기
        # 만약 특정 시점에 W 키를 떼고 싶다면 pyautogui.keyUp('w')를 추가
        # 0.3초 대기
        time.sleep(0.3)

# 함수 실행
automate_actions()