with open("base_stats.scsv", "r", encoding="utf-8") as base_stats_file: 
    # Level;Surveillance;Retrieval;Speed;Range;Favor
    base_stats = [f.split(";") for f in base_stats_file.read().split("\n")][1:]
    base_stats = [f for f in base_stats if f != [""]]

with open("parts.scsv", "r", encoding="utf-8") as parts_file: 
    # Type;Name;Surveillance;Retrieval;Speed;Range;Favor
    parts = [f.split(";") for f in parts_file.read().split("\n")][1:]
    parts = [f for f in parts if f != [""]]

    pressure_hulls = [f[1:] for f in parts if "Pressure Hull" in f[0]]
    sterns = [f[1:] for f in parts if "Stern" in f[0]]
    bows = [f[1:] for f in parts if "Bow" in f[0]]
    bridges = [f[1:] for f in parts if "Bridge" in f[0]]

import argparse

argparser = argparse.ArgumentParser(description="Calculate optimal part configuration, given a set of desired stats.")
argparser.add_argument("--surveillance", type=int, help="Desired surveillance stat.")
argparser.add_argument("--retrieval", type=int, help="Desired retrieval stat.")
argparser.add_argument("--speed", type=int, help="Desired speed stat.")
argparser.add_argument("--range", type=int, help="Desired range stat.")
argparser.add_argument("--favor", type=int, help="Desired favor stat.")
argparser.add_argument("--min-level", type=int, help="Minimum level to consider.")
argparser.add_argument("--max", type=int, help="Maximum number of builds to display.")
argparser.add_argument("--output_type", type=str, default="full", help="Output type: minimal, full.")
args = argparser.parse_args()

if args.surveillance is None: 
    args.surveillance = input("Surveillance: ")
    if args.surveillance == "": args.surveillance = 0
    else: args.surveillance = int(args.surveillance)

if args.retrieval is None:
    args.retrieval = input("Retrieval: ")
    if args.retrieval == "": args.retrieval = 0
    else: args.retrieval = int(args.retrieval) 

if args.speed is None:
    args.speed = input("Speed: ")
    if args.speed == "": args.speed = 0
    else: args.speed = int(args.speed)

if args.range is None:
    args.range = input("Range: ")
    if args.range == "": args.range = 0
    else: args.range = int(args.range)

if args.favor is None:
    args.favor = input("Favor: ")
    if args.favor == "": args.favor = 0
    else: args.favor = int(args.favor)

if args.min_level is None:
    args.min_level = input("Current submersible level: ")
    if args.min_level == "": args.min_level = 51
    else: args.min_level = int(args.min_level)

if args.max is None: 
    if args.output_type == "minimal": args.max = 15
    else: args.max = 3

print("")

# Check if all of the desired stats are zero
# If so, throw an error and exit. 
if args.surveillance == 0 and args.retrieval == 0 and args.speed == 0 and args.range == 0 and args.favor == 0: 
    print("Error: All desired stats are zero. Please specify at least one desired stat.")
    exit()

from itertools import product

combinations = []
for combination in product(pressure_hulls, sterns, bows, bridges):
    abbreviation = ""
    surveillance = 0
    retrieval = 0
    speed = 0
    range = 0
    favor = 0

    for part in combination:
        if "Shark" in part[0]: abbreviation += "S"
        elif "Unkiu" in part[0]: abbreviation += "U"
        elif "Whale" in part[0]: abbreviation += "W"
        elif "Coelacanth" in part[0]: abbreviation += "C"
        elif "Syldra" in part[0]: abbreviation += "Y"

        surveillance += int(part[1])
        retrieval += int(part[2])
        speed += int(part[3])
        range += int(part[4])
        favor += int(part[5])

    combinations.append([abbreviation, surveillance, retrieval, speed, range, favor])
# Initialize a list to store valid combinations across levels
valid_combinations = []
added_combinations = set()

# Iterate over each level's base stats
for stat in base_stats:
    current_level_combinations = []
    for combination in combinations:
        abbreviation, surveillance, retrieval, speed, range, favor = combination

        level = stat[0]
        surveillance += int(stat[1])
        retrieval += int(stat[2])
        speed += int(stat[3])
        range += int(stat[4])
        favor += int(stat[5])

        if int(level) < args.min_level: continue

        if surveillance >= args.surveillance and retrieval >= args.retrieval and speed >= args.speed and range >= args.range and favor >= args.favor:

            if abbreviation not in added_combinations:
                current_level_combinations.append([abbreviation, level, surveillance, retrieval, speed, range, favor])
                valid_combinations.append([abbreviation, level, surveillance, retrieval, speed, range, favor])
                added_combinations.add(abbreviation)

                # Stop adding more combinations if we reach the max number of desired combinations
                if len(valid_combinations) >= args.max:
                    break

    # Break the outer loop if we've reached the max number of desired combinations
    if len(valid_combinations) >= args.max:
        break

# Print an error if no valid combinations were found
if not valid_combinations:
    print("Error: No combination found that satisfies the desired stats.")
    exit()

# Sort valid combinations by level ascending, then speed descending, then range descending, then surveillance ascending, then retrieval ascending, then favor ascending

valid_combinations = sorted(valid_combinations, key=lambda x: (int(x[1]), -int(x[3]), -int(x[4]), int(x[2]), int(x[3]), int(x[5])))

if args.output_type == "minimal":
    for combination in valid_combinations:
        print(combination)

elif args.output_type == "full":
    for combination in valid_combinations:
        abbreviation = combination[0]
        print("Parts: ")
        if abbreviation[0] == "S": print("- Pressure Hull: Shark")
        elif abbreviation[0] == "U": print("- Pressure Hull: Unkiu")
        elif abbreviation[0] == "W": print("- Pressure Hull: Whale")
        elif abbreviation[0] == "C": print("- Pressure Hull: Coelacanth")
        elif abbreviation[0] == "Y": print("- Pressure Hull: Syldra")

        if abbreviation[1] == "S": print("- Stern: Shark")
        elif abbreviation[1] == "U": print("- Stern: Unkiu")
        elif abbreviation[1] == "W": print("- Stern: Whale")
        elif abbreviation[1] == "C": print("- Stern: Coelacanth")
        elif abbreviation[1] == "Y": print("- Stern: Syldra")

        if abbreviation[2] == "S": print("- Bow: Shark")
        elif abbreviation[2] == "U": print("- Bow: Unkiu")
        elif abbreviation[2] == "W": print("- Bow: Whale")
        elif abbreviation[2] == "C": print("- Bow: Coelacanth")
        elif abbreviation[2] == "Y": print("- Bow: Syldra")

        if abbreviation[3] == "S": print("- Bridge: Shark")
        elif abbreviation[3] == "U": print("- Bridge: Unkiu")
        elif abbreviation[3] == "W": print("- Bridge: Whale")
        elif abbreviation[3] == "C": print("- Bridge: Coelacanth")
        elif abbreviation[3] == "Y": print("- Bridge: Syldra")

        print(f"Level: {combination[1]}")
        print(f"Surveillance: {combination[2]}")
        print(f"Retrieval: {combination[3]}")
        print(f"Speed: {combination[4]}")
        print(f"Range: {combination[5]}")
        print(f"Favor: {combination[6]}")

        print("")