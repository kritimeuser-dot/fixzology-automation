# Fixzology - Face Lock + 7 Look Rotation
import datetime

STYLES = {
    0: "Monday - Traditional White Kurta + Black Nehru Jacket",
    1: "Tuesday - Black Shirt",
    2: "Wednesday - Coat",
    3: "Thursday - White Shirt",
    4: "Friday - Blue Shirt",
    5: "Saturday - Yellow Mustard",
    6: "Sunday - Grey",
}

today = datetime.datetime.now().weekday()
print("Aaj ka Style:", STYLES[today])
print("1. Sirf PIB / Court / ANI se khabar lo")
print("2. 3 jagah check karo, nahi mili to SKIP")
print("3. Hook + Kanoon + Question wali script banao")
print("4. Face Lock wali photo se video banao")
