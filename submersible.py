import pyautogui, pytesseract, re, datetime

image = pyautogui.screenshot()
image = image.crop((image.width * 0.35, image.height * 0.35, image.width * 0.65, image.height * 0.65))

# Undersea Shanty. (Rank: 89) (Voyage complete in 1d 9h 11m)
submersible_pattern = re.compile(r"([A-Za-z0-9\s]+)\. \(Rank: \d+\)")
voyage_pattern = re.compile(r"Voyage complete in (?:(\d+)d\s*)?(?:(\d+)h\s*)?(\d+)m")
completion_pattern = re.compile(r"Voyage complete")

text = pytesseract.image_to_string(image).split("\n")
text = list(filter(None, text))

with open("submersible.txt", "w", encoding="utf-8") as f: 
    for submersible in text: 
        sub_match = submersible_pattern.match(submersible)
        voyage_match = voyage_pattern.search(submersible)
        completion_match = completion_pattern.search(submersible)
        if sub_match: 
            # Compute epoch of completion
            if voyage_match: 
                days, hours, minutes = voyage_match.groups()
                sub_name = sub_match.groups()[0]
                days = int(days) if days else 0
                hours = int(hours) if hours else 0
                minutes = int(minutes)
                now = datetime.datetime.now().replace(second=0, microsecond=0)
                completion = now + datetime.timedelta(days=days, hours=hours, minutes=minutes)
                # Convert to unix time
                completion = int(completion.timestamp())
                f.write(f"**{sub_name}** Mission Complete: <t:{completion}:F> <t:{completion}:R>\n")

                # Print out completion time, using real time instead of relative time
                completion_time = datetime.datetime.fromtimestamp(completion).strftime("%Y-%m-%d %H:%M:%S")
                print(f"**{sub_name}** Mission Complete: {completion_time}")
            else: 
                sub_name = sub_match.groups()[0]
                f.write(f"**{sub_name}** Mission Complete: (now)\n")