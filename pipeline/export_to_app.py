#!/usr/bin/env python3
"""
Export scout.db -> parks-data.json in the exact shape the Site Scout app reads.
Each campground comes out with an explicit `sites` array (one entry per real
site), which the app already supports via cgSites().

By default only VERIFIED sites are exported. Pass --all to export everything
regardless of the verified flag (useful now, before anything is checked).

Run:  python3 export_to_app.py         # verified only
      python3 export_to_app.py --all   # everything
"""
import json, re, sqlite3, sys

DB, OUT = "scout.db", "parks-data.json"
ONLY_VERIFIED = "--all" not in sys.argv


def cap_list(text):
    """House style: capitalize the first letter of each comma- or middot-separated segment."""
    if not text: return text
    def cap_seg(seg):
        for i,ch in enumerate(seg):
            if ch.isalpha(): return seg[:i]+ch.upper()+seg[i+1:]
        return seg
    return " \u00b7 ".join(", ".join(cap_seg(p) for p in mid.split(", ")) for mid in text.split(" \u00b7 "))

def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    vfilter = "AND s.verified=1" if ONLY_VERIFIED else ""

    parks = []
    for p in con.execute("SELECT * FROM parks ORDER BY name").fetchall():
        park = dict(id=p["id"], name=p["name"], region=p["region"], url=p["url"],
                    blurb=p["blurb"], fishing=p["fishing"], fmz=p["fmz"],
                    facilities=json.loads(p["facilities"] or "[]"), campgrounds=[])
        cgs = con.execute("SELECT * FROM campgrounds WHERE park_id=? ORDER BY sort,name",
                          (p["id"],)).fetchall()
        trs = con.execute("SELECT name,length_km,difficulty,detail FROM trails WHERE park_id=? ORDER BY sort,name",(p["id"],)).fetchall()
        park["trails"] = [dict(name=t["name"], length=t["length_km"], difficulty=t["difficulty"], detail=t["detail"]) for t in trs]
        for c in cgs:
            rows = con.execute(
                f"SELECT label FROM sites s WHERE s.campground_id=? {vfilter} "
                "ORDER BY CAST(label AS INTEGER), label", (c["id"],)).fetchall()
            sites = [r["label"] for r in rows]
            if sites:
                park["campgrounds"].append(dict(id=c["name"], sub=cap_list(c["sub"]), sites=sites))
        # campground order comes from the seed's sort column (numeric ranges
        # ascending, backcountry and group areas last); do not re-sort here
        if not park["campgrounds"]:
            park["dayuse"] = True
        try:
            if p["backcountry"]:
                park["backcountry"] = True
        except (KeyError, IndexError):
            pass
        parks.append(park)

    json.dump(parks, open(OUT, "w"), ensure_ascii=False, indent=2)
    n = sum(len(c["sites"]) for pk in parks for c in pk["campgrounds"])
    print(f"Wrote {OUT}: {len(parks)} parks, {n} sites "
          f"[{'verified only' if ONLY_VERIFIED else 'ALL (unverified included)'}]")
    con.close()

if __name__ == "__main__":
    main()
