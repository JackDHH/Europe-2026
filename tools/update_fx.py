"""Writes fx.js (window.TRIP_FX): Australian dollars per 1 unit of each trip currency.
Source: Frankfurter (European Central Bank reference rates, updated each weekday ~16:00 CET). No API key."""
import json, urllib.request, time
CUR = ["EUR", "USD", "GBP", "DKK", "IDR"]
u = "https://api.frankfurter.dev/v1/latest?from=AUD&to=" + ",".join(CUR)
req = urllib.request.Request(u, headers={"User-Agent": "Europe-2026 trip planner"})
with urllib.request.urlopen(req, timeout=30) as r:
    j = json.load(r)
rates = {c: round(1 / float(j["rates"][c]), 8) for c in CUR}  # AUD per 1 unit
out = {"base": "AUD", "rates": rates, "date": j["date"], "source": "European Central Bank via Frankfurter", "updatedAt": int(time.time() * 1000)}
try:
    old = json.loads(open("fx.js", encoding="utf-8").read().split("=", 1)[1].rstrip().rstrip(";"))
    if old.get("date") == out["date"] and old.get("rates") == rates:
        print("FX unchanged", out["date"]); raise SystemExit(0)
except (FileNotFoundError, IndexError, ValueError):
    pass
open("fx.js", "w", encoding="utf-8").write("window.TRIP_FX = " + json.dumps(out) + ";\n")
print("FX", out["date"], rates)
