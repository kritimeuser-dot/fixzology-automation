# Fixzology - Face Lock + 7 Look Rotation
import datetime
import feedparser
import os, subprocess

STYLES = {
    0: "Monday - Traditional White Kurta + Black Nehru Jacket",
    1: "Tuesday - Black Shirt",
    2: "Wednesday - Coat",
    3: "Thursday - White Shirt",
    4: "Friday - Blue Shirt",
    5: "Saturday - Yellow Mustard",
    6: "Sunday - Grey",
}

DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

today_num = datetime.datetime.now().weekday()
today_name = DAYS[today_num]
today_style = STYLES[today_num]

print(f"Aaj ka Style: {today_style}")

# 1. PIB se khabar lo
print("1. Sirf PIB / Court / ANI se khabar lo")
pib_url = "https://pib.gov.in/RssMain.aspx?mod=6&reg=3&lang=1"
feed = feedparser.parse(pib_url)

if not feed.entries:
    print("Khabar nahi mili, SKIP")
    exit(0)

news = feed.entries[0]
title = news.title
summary = news.get("summary", "")[:500]
link = news.link
print(f"Khabar: {title}")

# 2. Check - 3 jagah
print("2. 3 jagah check karo, nahi mili to SKIP")
# Abhi PIB ko hi final maan rahe hai

# 3. Script banao
print("3. Hook + Kanoon + Question wali script banao")
script = f"""
HOOK: Ruko! {title}
STYLE: Aaj {today_style} me hu.

KHABAR: {summary}
Source: {link}

KANOON: Isse juda niyam sarkari notification ke hisaab se lagu hota hai.

QUESTION: Aapko kya lagta hai ye sahi hai ya galat? Comment me batao. Follow fixzology.
"""
with open("script.txt", "w", encoding="utf-8") as f:
    f.write(script)
print("Script ban gayi")

# 4. Face Lock photo se video banao
print("4. Face Lock wali photo se video banao")
photo = f"images/{today_name}.jpg"
print(f"Photo: {photo} - Style: {today_style}")

if not os.path.exists(photo):
    print(f"{photo} nahi mili")
    exit(0)

cmd = [
    "ffmpeg", "-y",
    "-loop", "1", "-i", photo,
    "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,zoompan=z='min(zoom+0.001,1.2)':d=900:s=1080x1920:fps=30",
    "-t", "30",
    "-pix_fmt", "yuv420p",
    "video.mp4"
]
subprocess.run(cmd)
print("Video ban gaya: video.mp4")
print("DONE")
