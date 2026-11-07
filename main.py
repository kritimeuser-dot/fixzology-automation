# Fixzology - TECH EDITION FINAL | 5AM + 5PM | Hook + Tech News + Voice
import datetime, os, subprocess, urllib.request, xml.etree.ElementTree as ET, random, re, requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
OUTPUT_VIDEO = os.path.join(BASE_DIR, "video.mp4")
OUTPUT_VIDEO_MUTE = os.path.join(BASE_DIR, "video_mute.mp4")
OUTPUT_SCRIPT = os.path.join(BASE_DIR, "script.txt")
OUTPUT_AUDIO = os.path.join(BASE_DIR, "voice.mp3")
OUTPUT_CAPTION = os.path.join(BASE_DIR, "caption.txt")

ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVEN_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")

# TECH SOURCES - Ab PIB band, sirf Tech
TECH_RSS = [
    "https://techcrunch.com/feed/",
    "https://www.gadgets360.com/rss/news",
    "https://www.theverge.com/rss/index.xml",
    "https://feeds.feedburner.com/TechCrunch/",
]

# HOOKS - Producer Level - Dar + Curiosity
HOOKS = [
    "Ruko! Ye wali khabar miss ki to pachtaoge, {title}",
    "99 percent logo ko iske baare me pata hi nahi hai, {title}",
    "Tumhara phone kal se aisa kyu chal raha hai? Wajah ye hai, {title}",
    "Instagram ne chupke se ye badal diya, {title}",
    "WhatsApp ka ye naya feature dekh ke tum shock ho jaoge, {title}",
    "Ye setting abhi ON nahi ki to tumhara phone khatre me hai, {title}",
    "AI ne aisa kar diya ki ab naukri ka kya hoga, {title}",
    "Ye trick sirf 1 percent logo ko pata hai, {title}",
]

STYLES = {0:"Monday - White Kurta + Black Nehru Jacket",1:"Tuesday - Black Shirt",2:"Wednesday - Coat",3:"Thursday - White Shirt",4:"Friday - Blue Shirt",5:"Saturday - Yellow Mustard",6:"Sunday - Grey"}
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

def log(m): print(f"[Fixzology-TECH] {m}", flush=True)

def clean_text(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    t = re.sub(r'&[^;]+;', ' ', t)
    t = re.sub(r'\s+', ' ', t).strip()
    return t[:900]

def fetch_tech_news():
    log("Tech khabar la rahe hai - TechCrunch / Gadgets360 / Verge se...")
    for url in TECH_RSS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=20) as r: data=r.read()
            root = ET.fromstring(data)
            items = root.findall(".//item")
            random.shuffle(items)
            for item in items[:5]:
                t = clean_text(item.findtext("title") or "")
                d = clean_text(item.findtext("description") or "")
                if t and len(t) > 20:
                    log(f"Khabar mili: {t[:80]}")
                    return {"title":t, "summary":d}
        except Exception as e:
            log(f"Fail {url} : {e}")
            continue
    return {"title":"AI ne naya kamaal kar diya","summary":"AI ki duniya me aaj bada update aaya hai. Naye tools aa rahe hai jo tumhara kaam 10 guna tez kar denge."}

def build_producer_script(news, style, slot):
    hook = random.choice(HOOKS).format(title=news['title'])
    # 55 sec ke liye lambi script
    script = f"""{hook}. Dekho dosto, baat ko seedha samjho. {news['summary']} Ab iska matlab tumhare liye kya hai? Matlab ye ki agar tumne ye setting abhi ON nahi ki to tum piche reh jaoge. Ye trick apne us dost ko bhejo jisko tech ka T bhi nahi pata. Aur haan, kal wali video me main ek aisa AI tool bataunga jo tumhara pura kaam 2 minute me kar dega. Uske liye follow dabana mat bhoolna, Fixzology."""
    open(OUTPUT_SCRIPT,"w",encoding="utf-8").write(script)
    # Caption bhi banate hai - Instagram ke liye
    caption = f"""{hook}

{news['summary'][:250]}

Ye trick us dost ko bhejo jiska phone hamesha hang hota hai 👇
Follow @fixzology - warna kal wali trick miss ho jayegi!

#Fixzology #TechNews #AI #WhatsApp #Instagram #Gadgets #TechTips #Viral"""
    open(OUTPUT_CAPTION,"w",encoding="utf-8").write(caption)
    log(f"Producer Script ban gayi - Hook: {hook[:60]}")
    return script

def make_voice(text):
    log("Voice bana rahe hai...")
    if ELEVEN_KEY and ELEVEN_VOICE_ID:
        try:
            url=f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
            r=requests.post(url, headers={"xi-api-key":ELEVEN_KEY,"Content-Type":"application/json"}, json={"text":text,"model_id":"eleven_multilingual_v2","voice_settings":{"stability":0.5,"similarity_boost":0.8}}, timeout=60)
            if r.status_code==200:
                open(OUTPUT_AUDIO,"wb").write(r.content); log("ElevenLabs Voice - Tumhari awaz"); return True
        except Exception as e: log(f"ElevenLabs fail: {e}")
    try:
        from gtts import gTTS
        gTTS(text=text, lang='hi', slow=False).save(OUTPUT_AUDIO)
        log("gTTS Voice ban gayi - Temporary")
        return True
    except Exception as e: log(f"gTTS fail: {e}")
    return False

def build_video(day_name, has_audio):
    log("Special Movement video bana rahe hai...")
    photo=os.path.join(IMAGES_DIR, f"{day_name}.jpg")
    if not os.path.exists(photo): log(f"Photo nahi mili: {photo}"); return False
    vf="scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,zoompan=z='1+0.12*sin(on/120)+0.08*sin(on/400)':x='iw/2-(iw/zoom/2)+30*sin(on/80)':y='ih/2-(ih/zoom/2)+20*sin(on/100)':d=1650:s=1080x1920:fps=30"
    subprocess.run(["ffmpeg","-y","-loop","1","-i",photo,"-vf",vf,"-t","55","-pix_fmt","yuv420p",OUTPUT_VIDEO_MUTE], capture_output=True)
    if has_audio and os.path.exists(OUTPUT_AUDIO):
        subprocess.run(["ffmpeg","-y","-i",OUTPUT_VIDEO_MUTE,"-i",OUTPUT_AUDIO,"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-shortest",OUTPUT_VIDEO], capture_output=True)
        log("Video + Voice merge ho gaya")
    else:
        os.rename(OUTPUT_VIDEO_MUTE, OUTPUT_VIDEO)
    return os.path.exists(OUTPUT_VIDEO)

def main():
    now=datetime.datetime.now(); slot="Subah 5 AM" if now.hour<12 else "Sham 5 PM"
    today=DAYS[now.weekday()]; style=STYLES[now.weekday()]
    log(f"START | {slot} | {today} | {style}")
    news=fetch_tech_news()
    script=build_producer_script(news, style, slot)
    has_audio=make_voice(script)
    ok=build_video(today, has_audio)
    log("DONE - Tech Reel Ready" if ok else "FAIL")

if __name__=="__main__": main()
