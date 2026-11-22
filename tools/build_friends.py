import json, glob, os, re, datetime
BASE = os.path.dirname(os.path.abspath(__file__))
STOPS = [
 {"id":"mel0","city":"Melbourne","country":"Australia","flag":"🇦🇺","tz":"Australia/Melbourne","ll":[-37.8136,144.9631],"in":"2026-11-28","out":"2026-11-29","kind":"home","note":"Bags packed, off to the airport!"},
 {"id":"lax","city":"Los Angeles","country":"USA","flag":"🇺🇸","tz":"America/Los_Angeles","ll":[34.0522,-118.2437],"in":"2026-11-29","out":"2026-11-30","kind":"stopover","note":"A day's stopover on the way to London"},
 {"id":"lon","city":"London","country":"England","flag":"🇬🇧","tz":"Europe/London","ll":[51.5074,-0.1278],"in":"2026-11-30","out":"2026-12-05"},
 {"id":"par","city":"Paris","country":"France","flag":"🇫🇷","tz":"Europe/Paris","ll":[48.8566,2.3522],"in":"2026-12-05","out":"2026-12-09"},
 {"id":"str","city":"Strasbourg","country":"France","flag":"🇫🇷","tz":"Europe/Paris","ll":[48.5734,7.7521],"in":"2026-12-09","out":"2026-12-11"},
 {"id":"ghe","city":"Ghent","country":"Belgium","flag":"🇧🇪","tz":"Europe/Brussels","ll":[51.0543,3.7174],"in":"2026-12-11","out":"2026-12-15"},
 {"id":"nur","city":"Nürnberg","country":"Germany","flag":"🇩🇪","tz":"Europe/Berlin","ll":[49.4521,11.0767],"in":"2026-12-15","out":"2026-12-18"},
 {"id":"fre","city":"Freising (near Munich)","country":"Germany","flag":"🇩🇪","tz":"Europe/Berlin","ll":[48.4029,11.7488],"in":"2026-12-18","out":"2026-12-22"},
 {"id":"wer","city":"Werfenweng (the Alps)","country":"Austria","flag":"🇦🇹","tz":"Europe/Vienna","ll":[47.4626,13.2580],"in":"2026-12-22","out":"2026-12-26","note":"A white Christmas in the mountains ⛄"},
 {"id":"vie","city":"Vienna","country":"Austria","flag":"🇦🇹","tz":"Europe/Vienna","ll":[48.2082,16.3738],"in":"2026-12-26","out":"2026-12-30"},
 {"id":"cph","city":"Copenhagen","country":"Denmark","flag":"🇩🇰","tz":"Europe/Copenhagen","ll":[55.6761,12.5683],"in":"2026-12-30","out":"2027-01-03","note":"New Year's Eve at Tivoli Gardens 🎆"},
 {"id":"auh","city":"Abu Dhabi (in transit)","country":"UAE","flag":"🇦🇪","tz":"Asia/Dubai","ll":[24.4539,54.3773],"in":"2027-01-03","out":"2027-01-04","kind":"stopover","note":"Flying from Europe to Bali"},
 {"id":"bal","city":"Bali","country":"Indonesia","flag":"🇮🇩","tz":"Asia/Makassar","ll":[-8.6705,115.2126],"in":"2027-01-04","out":"2027-01-10","note":"Pool, beach and a well-earned rest 🏝"},
 {"id":"home","city":"Home","country":"Australia","flag":"🇦🇺","tz":"Australia/Melbourne","ll":[-38.3436,143.5850],"in":"2027-01-10","out":"2027-01-12","kind":"home","note":"Flying home overnight and a big sleep-in 😴"},
]
SKIP_TYPES = {"Getting around","Other"}
def clean(t):
    t = re.sub(r"^(Vienna|Copenhagen|Bruges|Antwerp|Munich|London|Paris|Harry Potter): *", lambda m: "" if m.group(1)!="Harry Potter" else "Harry Potter: ", t)
    t = t.replace("at Gut Wenghof"," at the resort").replace("Gut Wenghof","the resort")
    t = re.sub(r"\s*\((?:TBA|still to book|tickets \+ audio guides|9 pm|\+ river cruise)\)","",t)
    t = t.replace(": 2-park tickets + Premier Access Ultimate"," 🏰").replace("Moulin Rouge: Féerie show","Moulin Rouge show")
    t = re.sub(r"\s{2,}"," ",t).strip()
    return t[:1].upper()+t[1:]
items = {}
for f in glob.glob(os.path.join(BASE,"dump2/plans/*.json")):
    x = json.load(open(f)); x = x.get("data", x); pid = os.path.basename(f)[:-5]
    if x.get("status") not in ("Booked","Planned") or not x.get("date"): continue
    if x.get("type") in SKIP_TYPES or pid.startswith("home-") or pid in ("hp-walk","hp-coach-back","hp-back","fre-day21-pick"): continue
    if pid == "jcv6337guqa3osldwcls": t = "Harry Potter: Warner Bros Studio Tour 🧙"
    elif pid == "hp-studio": continue
    else: t = clean(x.get("title",""))
    if re.search(r"\b[A-Z0-9]{6,}\b", t) and not re.search(r"[a-z]", t): continue
    tm = x.get("time") or "99"
    items.setdefault(x["date"], []).append((tm, t))
DAYS = {d: [{"t": t, "am": tm < "12:00"} for tm, t in sorted(v)] for d, v in items.items()}
# travel days (no times, no flight numbers)
TRAVEL = {"2026-11-29":"✈ Melbourne → Sydney → Los Angeles","2026-11-30":"✈ Overnight to London","2026-12-05":"🚄 Eurostar to Paris","2026-12-09":"🚄 Fast train to Strasbourg",
 "2026-12-11":"🚆 Trains to Ghent","2026-12-15":"🚆 Train to Nürnberg","2026-12-18":"🚆 Train to Freising","2026-12-22":"🚆 Train to the Alps (via Salzburg)","2026-12-26":"🚆 Train to Vienna",
 "2026-12-30":"✈ Fly to Copenhagen","2027-01-03":"✈ Copenhagen → Abu Dhabi → Bali (overnight)","2027-01-04":"🏝 Land in Bali","2027-01-10":"✈ Fly home to Melbourne","2027-01-11":"🏡 Home sweet home"}
# journal (only posts marked public; photos must already be processed into friends/photos/<id>.jpg)
PLAN_TITLES = {}
for f in glob.glob(os.path.join(BASE,"dump2/plans/*.json")):
    if os.path.basename(f).startswith("."): continue
    x = json.load(open(f)); x = x.get("data", x); PLAN_TITLES[os.path.basename(f)[:-5]] = clean(x.get("title",""))
JOURNAL = []
for f in sorted(glob.glob(os.path.join(BASE,"journal_dump/journal/*.json"))):
    if os.path.basename(f).startswith("."): continue
    x = json.load(open(f)); x = x.get("data", x)
    if x.get("public") is False or not re.match(r"^\d{4}-\d{2}-\d{2}$", x.get("date","")): continue
    photos = []
    for ph in x.get("photos") or []:
        pid = ph.get("id","")
        if not re.match(r"^[a-f0-9]{32}$", pid, re.I) or not os.path.exists(os.path.join(BASE,"friends/photos",pid+".jpg")): continue
        cap = (ph.get("caption") or "").strip() or PLAN_TITLES.get(ph.get("planId",""), "")
        photos.append({"src":"photos/"+pid+".jpg","caption":cap[:140]})
    JOURNAL.append({"date":x["date"],"stay":x.get("stay",""),"title":(x.get("title") or "")[:120],"text":(x.get("text") or "")[:4000],"photos":photos,"at":x.get("createdAt",0)})
JOURNAL.sort(key=lambda j:(j["date"], j["at"]), reverse=True)
data = {"journal":JOURNAL,"stops":STOPS,"days":DAYS,"travel":TRAVEL,"start":"2026-11-29","end":"2027-01-11","updated":datetime.date.today().isoformat()}
tpl = open(os.path.join(BASE,"friends_template.html"),encoding="utf-8").read()
out = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False))
open(os.path.join(BASE,"friends/index.html"),"w",encoding="utf-8").write(out)
print("days with highlights:", len(DAYS), "items:", sum(len(v) for v in DAYS.values()))
