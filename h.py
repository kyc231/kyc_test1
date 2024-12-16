import pyautogui
import keyboard
import time

# 회오리 점프 매크로 함수
def tornado_jump():
    # 약간의 지연 (매크로 실행 준비 시간)
    time.sleep(0.5)
    
    # 점프 (스페이스바 누르기)
    pyautogui.press('space')
    
    # 회전 (방향키 왼쪽 또는 오른쪽 누르기)
    for _ in range(10):  # 10번 반복하여 회전
        pyautogui.press('left')  # 왼쪽 방향으로 회전, 'right'으로 변경 가능
        time.sleep(0.1)  # 회전 속도 조절

    # 회전 후 멈춤
    pyautogui.keyUp('left')

# Alt+1을 누르면 tornado_jump 함수 실행
keyboard.add_hotkey('f8', tornado_jump)

# 프로그램이 종료되지 않도록 대기
print("Alt+8을 누르면 회오리 점프 매크로가 실행됩니다.")
keyboard.wait('esc')  # 사용자가 'esc'를 누르면 프로그램 종료
