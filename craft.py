import pyautogui, time, argparse, sys

parser = argparse.ArgumentParser(description='Run a macro in Final Fantasy XIV')
parser.add_argument('-s', '--slot', type=int, help='Macro slot to run (1-12)', required=False)
parser.add_argument('-n', '--numLoops', type=int, help='Number of times to run the macro', required=False)
parser.add_argument('-t', '--sleepTime', type=int, help='Time to sleep between macro runs', nargs='+', required=False)
parser.add_argument('--delay', type=int, help='Number of seconds to delay crafting start by', default=0, required=False)
parser.add_argument('--food', type=int, help='Remaining duration of food buff', default=0, required=False)
args = parser.parse_args()

# If the user didn't specify a slot, ask them for one.
if args.slot is None:
    args.slot = int(input('Macro slot to run (1-10): '))

# If the user didn't specify a sleep time, ask them for one.
if args.sleepTime is None:
    args.sleepTime = input('Time to sleep between macro runs: ')
    if ' ' in args.sleepTime:
        args.sleepTime = [int(x) for x in args.sleepTime.split()]
    else:
        args.sleepTime = [int(args.sleepTime)]

# If the user didn't specify a number of loops, ask them for one.
if args.numLoops is None:
    # Maximum loops in 30 minutes is equal to 1800 / (sleepTime + 6)
    # Maximum loops in 60 minutes is equal to 3600 / (sleepTime + 6)

    # If food buff was not given, show 30 min and 60 min timers
    if args.food == 0:
        loops_30 = 1800 // (sum(args.sleepTime) + 6)
        loops_60 = 3600 // (sum(args.sleepTime) + 6)

        print(f'Maximum loops in 30 minutes: {loops_30}')
        print(f'Maximum loops in 60 minutes: {loops_60}')

    else: 
        loops = args.food * 60 // (sum(args.sleepTime) + 6)
        print(f'Maximum loops in {args.food} minutes: {loops}')

    args.numLoops = int(input('Number of times to run the macro: '))

if len(args.sleepTime) > 1:
    args.sleepTime = [int(x) for x in args.sleepTime]

else: 
    args.sleepTime = int(args.sleepTime[0])

slot = args.slot
numLoops = args.numLoops
sleepTime = args.sleepTime

print('')

# Define the coordinates for the buttons we're going to click.
button_size = 80

macro_coords = (900 + (slot - 1) % 2 * button_size, 1310 - (slot - 1) // 2 * button_size)
double_coords = (macro_coords[0] + button_size, macro_coords[1]) if slot % 2 != 0 else None

synthesize_coords = (1080, 825)

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