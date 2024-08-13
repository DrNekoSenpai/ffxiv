num_characters = 200
max_arrow_keys = 25

channel = "party" # fc, party, echo, say

if channel == "party": sound_effect = False
else: sound_effect = True

import random, pyautogui

pyautogui.hotkey('alt', 'tab')
pyautogui.hotkey('enter')
if channel == "fc": pyautogui.typewrite('/fc ')
elif channel == "party": pyautogui.typewrite('/p ')
elif channel == "echo": pyautogui.typewrite('/echo ')
elif channel == "say": pyautogui.typewrite('/s ')
elif channel == "shout": pyautogui.typewrite('/shout ')

for i in range(num_characters):
    sel = random.randint(0, 100)
    if sel < 5: 
        pyautogui.hotkey('tab')

        for i in range(random.randint(1, max_arrow_keys)):
            arrow_key = random.randint(0, 3)
            if arrow_key == 0: pyautogui.hotkey('up')
            elif arrow_key == 1: pyautogui.hotkey('down')
            elif arrow_key == 2: pyautogui.hotkey('left')
            elif arrow_key == 3: pyautogui.hotkey('right')

        pyautogui.hotkey('enter')

    elif sel < 35:
        num_key = random.randint(0, 9)
        pyautogui.typewrite(f"{num_key}")

    elif sel < 65:
        letter_key = random.randint(0, 26)
        pyautogui.typewrite(chr(65 + letter_key))

    elif sel < 95 or sound_effect: 
        letter_key = random.randint(0, 26)
        pyautogui.typewrite(chr(97 + letter_key))

    else: 
        sound_effect = random.randint(1, 16)
        pyautogui.typewrite(f"<se.{sound_effect}>")
        sound_effect = True