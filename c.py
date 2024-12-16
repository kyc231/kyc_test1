import pyautogui
import keyboard
import time
import threading

# 전역 변수 설정
running = False

# 마우스 클릭
def mouse_click():
    pyautogui.click()

# 스페이스 바 누르기
def press_space():
    pyautogui.press('space')

# 작업을 반복 수행하는 함수
def task():
    while running:
        mouse_click()
        #time.sleep(0.5)  # 마우스 클릭 후 지연
        press_space()
        #time.sleep(0.5)  # 스페이스 바 누른 후 지연

# Tab 키 이벤트 핸들러
def toggle_task():
    global running
    if running:
        running = False
        print("작업 중지")
    else:
        running = True
        print("작업 시작")
        threading.Thread(target=task).start()

# 메인 함수
def main():
    # Tab 키가 눌릴 때마다 toggle_task 함수 실행
    keyboard.add_hotkey('tab', toggle_task)

    # 프로그램이 종료되지 않도록 유지
    print("Tab 키를 눌러 작업을 시작하거나 중지하세요.")
    keyboard.wait('esc')  # ESC 키를 누르면 프로그램 종료

if __name__ == "__main__":
    main()
