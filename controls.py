import pyautogui

pyautogui.FAILSAFE = False

def controls(fingers, dx, dy, done, key_mode):
    if fingers == 0:
        if key_mode:
            if dx > 20:
                print("Right arrow key")
                pyautogui.press('right')
            elif dx < -20:
                print("Left arrow key")
                pyautogui.press('left')
            if dy > 20:
                print("Up arrow key")
                pyautogui.press('up')
            elif dy < -20:
                print("Down arrow key")
                pyautogui.press('down')
        else:
            print("Drag mouse: ", dx, dy)
            pyautogui.dragRel(dx, dy, duration=0.5)
        done = [False, False, False]
    elif fingers == 1 and done[0] == False:
        if key_mode:
            print("Space key")
            pyautogui.press('space')
        else:
            print("Single click")
            pyautogui.click()
        done = [True, False, False]
    elif fingers == 2 and done[1] == False:
        print("Double click")
        pyautogui.doubleClick()
        done = [False, True, False]
    elif fingers == 3:
        if dy > 10:
            pyautogui.scroll(1)
        elif dy < -10:
            pyautogui.scroll(-1)
        done = [False, False, False]
    elif fingers == 4 and done[2] == False:
        done = [False, False, True]
        key_mode = not key_mode
    elif fingers == 5:
        print("Move mouse: ", dx, dy)
        pyautogui.moveRel(dx, dy)
        done = [False, False, False]

    return done, key_mode
