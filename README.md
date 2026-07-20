# Site Journal

A personal Ontario Parks campsite journal by Katsuma Onishi. Walk a campground, rate the sites, note which ones to book next time.

**Live app:** host this repo with GitHub Pages and open `index.html` (works offline once added to your home screen).

## What's here
- `index.html` - the whole app (single file: HTML, CSS, JS, embedded park data)
- `parks-data.json` - park/campground/site/trail data (also embedded in index.html)
- `service-worker.js`, `manifest.json`, icons - PWA install + offline support
- `pipeline/` - the SQL data pipeline that generates parks-data.json
  - `build_db.py` seeds `scout.db` from the data tables in the file
  - `export_to_app.py --all` writes `parks-data.json`

## Updating park data
```
cd pipeline
python3 build_db.py
python3 export_to_app.py --all
cp parks-data.json ../parks-data.json
```
Then re-embed the JSON into index.html (the app also fetches parks-data.json in the background) and bump the cache version in service-worker.js.

Currently: 28 parks, ~9,270 sites, 92 trails, 29 unlockable themes.
