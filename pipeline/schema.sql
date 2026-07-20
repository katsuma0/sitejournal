-- Site Scout data model: parks -> campgrounds -> sites, plus trails per park.
PRAGMA foreign_keys = ON;

CREATE TABLE parks (
  id TEXT PRIMARY KEY, name TEXT NOT NULL, region TEXT, url TEXT,
  blurb TEXT, fishing TEXT, fmz TEXT, sort INTEGER DEFAULT 0, facilities TEXT
);
CREATE TABLE campgrounds (
  id INTEGER PRIMARY KEY AUTOINCREMENT, park_id TEXT NOT NULL REFERENCES parks(id),
  name TEXT NOT NULL, sub TEXT, sort INTEGER DEFAULT 0
);
CREATE TABLE sites (
  id INTEGER PRIMARY KEY AUTOINCREMENT, campground_id INTEGER NOT NULL REFERENCES campgrounds(id),
  label TEXT NOT NULL, verified INTEGER DEFAULT 0, source TEXT
);
CREATE TABLE trails (
  id INTEGER PRIMARY KEY AUTOINCREMENT, park_id TEXT NOT NULL REFERENCES parks(id),
  name TEXT NOT NULL, length_km REAL, difficulty TEXT, detail TEXT, sort INTEGER DEFAULT 0
);
CREATE INDEX idx_cg_park  ON campgrounds(park_id);
CREATE INDEX idx_site_cg  ON sites(campground_id);
CREATE INDEX idx_site_lbl ON sites(label);
CREATE INDEX idx_trail_park ON trails(park_id);
