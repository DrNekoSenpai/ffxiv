with open("base_stats.scsv", "r", encoding="utf-8") as base_stats_file: 
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
args = argparser.parse_args()

if args.surveillance is None: 
    args.surveillance = input("Surveillance: ")
    if args.surveillance == "": 
        args.surveillance = 0

if args.retrieval is None:
    args.retrieval = input("Retrieval: ")
    if args.retrieval == "": 
        args.retrieval = 0

if args.speed is None:
    args.speed = input("Speed: ")
    if args.speed == "": 
        args.speed = 0

if args.range is None:
    args.range = input("Range: ")
    if args.range == "": 
        args.range = 0

if args.favor is None:
    args.favor = input("Favor: ")
    if args.favor == "": 
        args.favor = 0

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

print(f"Total combinations: {len(combinations)}")