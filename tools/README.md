# Rebuilding the site

Used by Claude to regenerate `index.html` from the family travel planner.

1. Export the planner's `plans` collection to `dump2/plans/` and the `journal` collection to `journal_dump/journal/` (one JSON file per document), next to these scripts.
2. Download each public journal photo (by asset id) into a folder, then run `python3 -I process_photos.py <that folder>`. This re-encodes every photo with **all metadata stripped** (no GPS, camera or time data) into `friends/photos/`.
3. Run `python3 build_friends.py` to write `friends/index.html`.
4. Copy `friends/index.html` and `friends/photos/` to the root of this repo and commit.

Only journal posts marked "show on the family website" are included. Booking references, prices, addresses and exact times are never written to the site.
