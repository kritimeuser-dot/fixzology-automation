# Fixzology - TECH EDITION | Producer Level
import datetime, os, urllib.request, xml.etree.ElementTree as ET, random

TECH_RSS = [
    "https://techcrunch.com/feed/",
    "https://www.gadgets360.com/rss/news",
    "https://www.theverge.com/rss/index.xml",
]

HOOKS = [
    "Ruko! Ye wali khabar miss ki to pachtaoge, {title}",
    "99% logo ko iske baare me pata hi nahi hai, {title}",
    "Tumhara phone kal se aisa kyu chal raha hai? Wajah ye hai, {title}",
    "Instagram ne chupke se ye badal diya, {title}",
    "WhatsApp ka ye naya feature dekh ke tum shock ho jaoge, {title}",
]

def fetch_tech_news():
    for url in TECH_RSS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r: data=r.read()
            root=ET.fromstring(data)
            for item in root.findall(".//item")[:5]:
                t=(item.findtext("title") or "").strip()
                d=(item.findtext("description") or "").strip()
                if t and len(t)>20:
                    return {"title":t, "summary":d[:900]}
        except: continue
    return {"title":"AI ne naya kamaal kar diya","summary":"AI ki duniya me aaj bada update aaya hai."}

def build_producer_script(news):
    hook = random.choice(HOOKS).format(title=news['title'])
    script = f"""{hook}. Dekho dosto, baat ko seedha samjho. {news['summary']} Ab iska matlab tumhare liye kya hai? Matlab ye ki agar tumne ye setting abhi ON nahi ki to tum piche reh jaoge. Ye trick apne us dost ko bhejo jisko tech ka T bhi nahi pata. Aur haan, kal wali video me main ek aisa AI tool bataunga jo tumhara pura homework 2 minute me kar dega. Uske liye follow dabana mat bhoolna, Fixzology."""
    open("script.txt","w",encoding="utf-8").write(script)
    return script
