import pyautogui, time, argparse, sys

parser = argparse.ArgumentParser(description='Run a macro in Final Fantasy XIV')
parser.add_argument('-s', '--slot', type=int, help='Macro slot to run (1-12)', required=False)
parser.add_argument('-n', '--numLoops', type=int, help='Number of times to run the macro', required=False)
parser.add_argument('-t', '--sleepTime', type=int, help='Time to sleep between macro runs', nargs='+', required=False)
parser.add_argument('--delay', type=int, help='Number of seconds to delay crafting start by', default=0, required=False)
parser.add_argument("--sync", action="store_true", help="Sync button", required=False)
args = parser.parse_args()

# If the user didn't specify a slot, ask them for one.
if args.slot is None:
    args.slot = int(input('Macro slot to run (1-12): '))

# If the user didn't specify a number of loops, ask them for one.
if args.numLoops is None:
    args.numLoops = int(input('Number of times to run the macro: '))

# If the user didn't specify a sleep time, ask them for one.
if args.sleepTime is None:
    args.sleepTime = input('Time to sleep between macro runs: ')
    if ' ' in args.sleepTime:
        args.sleepTime = [int(x) for x in args.sleepTime.split()]
    else:
        args.sleepTime = [int(args.sleepTime)]

if len(args.sleepTime) > 1:
    args.sleepTime = [int(x) for x in args.sleepTime]

slot = args.slot
numLoops = args.numLoops
sleepTime = args.sleepTime

print('')

# Define the coordinates for the buttons we're going to click.
button_size = 90

macro_coords = (960 + (slot - 1) * button_size, 1170)
double_coords = (960 + slot * button_size, 1170)
synthesize_coords = (1080, 825)
sync_button = (1480, 1265)

if numLoops != 1: 
    if isinstance(sleepTime, int):
        sleepTime += 3
        est_time_remaining = (sleepTime + 3) * numLoops
    else: 
        sleepTime[1] += 3
        est_time_remaining = (sleepTime[0] + sleepTime[1] + 3) * numLoops

else:
    if isinstance(sleepTime, int):
        est_time_remaining = sleepTime
    else:
        est_time_remaining = sleepTime[0] + sleepTime[1]

# If the delay flag is set, print the delay time remaining, but don't run the macro.
if args.delay > 0:
    print(f'Delaying macro start by {args.delay} seconds...')
    time.sleep(args.delay)

# Hit the sync button
if args.sync:
    pyautogui.moveTo(sync_button)
    pyautogui.mouseDown(button='left')
    time.sleep(0.25)
    pyautogui.mouseUp(button='left')
    time.sleep(1)

if isinstance(sleepTime, int):
    # We loop through the number of times the user specified.
    for i in range(numLoops):
        # Print out the current iteration and estimated time remaining.
        print(f'Iteration: {i+1} / {numLoops}')
        print(f'Estimated time remaining: {int(est_time_remaining / 60)} minutes, {int(est_time_remaining % 60)} seconds')
        print("")
        # Move the mouse to the Synthesize button and click it.
        pyautogui.moveTo(synthesize_coords)
        pyautogui.mouseDown(button='left')
        time.sleep(0.25)
        pyautogui.mouseUp(button='left')
        time.sleep(2.5)

        # Move the mouse to the corresponding macro button and click it. 
        pyautogui.moveTo(macro_coords)
        pyautogui.mouseDown(button='left')
        time.sleep(0.25)
        pyautogui.mouseUp(button='left')
        est_time_remaining -= sleepTime + 3

        # If we have more iterations to go, sleep for the specified amount of time.
        if i != numLoops - 1: time.sleep(sleepTime)

else: 
    for i in range(numLoops): 
        print(f'Iteration: {i+1} / {numLoops}')
        print(f'Estimated time remaining: {int(est_time_remaining / 60)} minutes, {int(est_time_remaining % 60)} seconds')
        print("")
        # Move the mouse to the Synthesize button and click it.
        pyautogui.moveTo(synthesize_coords)
        pyautogui.mouseDown(button='left')
        time.sleep(0.25)
        pyautogui.mouseUp(button='left')
        time.sleep(2.5)

        # Move the mouse to the FIRST macro button and click it.
        pyautogui.moveTo(macro_coords)
        pyautogui.mouseDown(button='left')
        time.sleep(0.25)
        pyautogui.mouseUp(button='left')
        time.sleep(sleepTime[0])

        # Move the mouse to the SECOND macro button and click it.
        pyautogui.moveTo(double_coords)
        pyautogui.mouseDown(button='left')
        time.sleep(0.25)
        pyautogui.mouseUp(button='left')
        if i != numLoops - 1: time.sleep(sleepTime[1])

        est_time_remaining -= sleepTime[0] + sleepTime[1] + 3