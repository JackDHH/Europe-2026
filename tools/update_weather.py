"""Writes weather.js (window.TRIP_WEATHER) for wherever the family is today. Run by the GitHub Action every few hours."""
import json, urllib.request, datetime, time
from zoneinfo import ZoneInfo
STOPS = [  # (planner key, place, tz, lat, lng, first day, day after)
 ("lax","Los Angeles","America/Los_Angeles",34.0522,-118.2437,"2026-11-01","2026-11-30"),
 ("lon","London","Europe/London",51.5074,-0.1278,"2026-11-30","2026-12-05"),
 ("par","Paris","Europe/Paris",48.8566,2.3522,"2026-12-05","2026-12-09"),
 ("str","Strasbourg","Europe/Paris",48.5734,7.7521,"2026-12-09","2026-12-11"),
 ("ghe","Ghent","Europe/Brussels",51.0543,3.7174,"2026-12-11","2026-12-15"),
 ("nur","Nürnberg","Europe/Berlin",49.4521,11.0767,"2026-12-15","2026-12-18"),
 ("fre","Freising","Europe/Berlin",48.4029,11.7488,"2026-12-18","2026-12-22"),
 ("wer","Werfenweng","Europe/Vienna",47.4626,13.258,"2026-12-22","2026-12-26"),
 ("vie","Vienna","Europe/Vienna",48.2082,16.3738,"2026-12-26","2026-12-30"),
 ("cph","Copenhagen","Europe/Copenhagen",55.6761,12.5683,"2026-12-30","2027-01-03"),
 ("bal","Bali","Asia/Makassar",-8.7905,115.2265,"2027-01-03","2027-01-12"),
]
def wmo(c):
    return ("clear","Clear") if c==0 else ("partly cloudy","Partly cloudy") if c<=2 else ("overcast","Cloudy") if c==3 else ("fog","Fog") if c<=48 else ("drizzle","Drizzle") if c<=57 else ("rain","Rain") if c<=67 else ("snow","Snow") if c<=77 else ("rain showers","Showers") if c<=82 else ("snow showers","Snow showers") if c<=86 else ("thunderstorm","Thunderstorm")
def get(lat, lng):
    u = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current=temperature_2m,apparent_temperature,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto&forecast_days=4"
    with urllib.request.urlopen(u, timeout=30) as r: return json.load(r)
now = datetime.datetime.now(datetime.timezone.utc)
stop = None
for s in STOPS:
    d = now.astimezone(ZoneInfo(s[2])).date().isoformat()
    if s[5] <= d < s[6]: stop = s; break
if stop is None: stop = STOPS[0] if now.date().isoformat() < "2026-11-30" else STOPS[-1]
j = get(stop[3], stop[4]); c = wmo(int(j["current"]["weather_code"]))
m = get(-37.8136, 144.9631)
out = {"key": stop[0], "place": stop[1], "temp": j["current"]["temperature_2m"], "feels": j["current"]["apparent_temperature"], "condition": c[0], "conditionText": c[1],
       "updatedAt": int(time.time() * 1000), "melbourne": m["current"]["temperature_2m"],
       "daily": [{"date": t, "high": j["daily"]["temperature_2m_max"][i], "low": j["daily"]["temperature_2m_min"][i], "rain": round(j["daily"]["precipitation_probability_max"][i] or 0)} for i, t in enumerate(j["daily"]["time"])]}
open("weather.js", "w", encoding="utf-8").write("window.TRIP_WEATHER = " + json.dumps(out, ensure_ascii=False) + ";\n")
print(stop[1], out["temp"])
