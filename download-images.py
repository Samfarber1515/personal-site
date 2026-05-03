#!/usr/bin/env python3
"""Download every remote image referenced by index.html into ./images/.

Usage:
    python3 download-images.py

No third-party deps required. Re-runnable: skips files that already exist.
"""
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

MAPPING = [
    ('https://i.imgur.com/uWTZMsH.jpg', 'images/zealot-moment-1.jpg'),
    ('https://i.imgur.com/tEoCCsX.jpg', 'images/zealot-moment-2.jpg'),
    ('https://i.imgur.com/YKcbDyz.jpg', 'images/zealot-moment-3.jpg'),
    ('https://gcdnb.pbrd.co/images/3Bxytggh195Y.png?o=1', 'images/tiktok-viral-content.png'),
    ('https://i.imgur.com/IP0Jd8r.jpg', 'images/tweet-tapestry-store-listing.jpg'),
    ('https://i.imgur.com/yaXRHeN.jpg', 'images/tweet-tapestry-store-page.jpg'),
    ('https://gcdnb.pbrd.co/images/cKvnpnpRotP8.png?o=1', 'images/butler-football.png'),
    ('https://i.imgur.com/QoulQZC.jpg', 'images/underground-madden-gambling-ring.jpg'),
    ('https://i.imgur.com/6AGcmO0.jpg', 'images/world-record-pencil-attempt.jpg'),
    ('https://i.imgur.com/PmaH6Ew.jpg', 'images/unlimited-money-glitch.jpg'),
    ('https://gcdnb.pbrd.co/images/zqUkkVTgAsBl.jpg?o=1', 'images/first-bass-caught-while-ice-fishing.jpg'),
    ('https://i.imgur.com/KE3mTMA.jpeg', 'images/skiing-in-vail.jpeg'),
    ('https://i.imgur.com/qDEAVXT.png', 'images/getting-ready-to-pitch-10-vcs-in-one-day-in-nyc.png'),
    ('https://i.imgur.com/MwrUcg5.png', 'images/me-after-getting-zero-yeses-from-vcs.png'),
    ('https://i.imgur.com/fst44J5.jpeg', 'images/skiing-in-banff.jpeg'),
    ('https://i.imgur.com/94uuft0.jpg', 'images/go-cubs.jpg'),
    ('https://i.imgur.com/fJkDjix.jpg', 'images/giving-a-speech-at-butler-to-300-entrepreneurs-and-meeting-alex-palou.jpg'),
    ('https://i.imgur.com/oZltK7A.jpg', 'images/tea-ceremony-at-fairmont-suites-in-banff.jpg'),
    ('https://i.imgur.com/Q7xJNnu.jpg', 'images/highline-2025-aka-the-coolest-b2b-conference-ever.jpg'),
    ('https://i.imgur.com/ry3WJ0x.jpg', 'images/whitewater-rafting-at-highline-2025.jpg'),
    ('https://i.imgur.com/sJH3Rxi.jpg', 'images/sarah-and-my-engagement-party-at-zhivago.jpg'),
    ('https://i.imgur.com/L428IK2.jpg', 'images/best-takeoff-gift-ever-from-sarah-ahead-of-the-acquisition-announcement.jpg'),
    ('https://i.imgur.com/OLba6Kj.jpg', 'images/hanging-at-sharan-s-adult-prom-event-in-a-random-nyc-warehouse.jpg'),
    ('https://i.imgur.com/OfCi5BJ.jpg', 'images/island-tour-in-croatia-for-sarah-s-birthday.jpg'),
    ('https://i.imgur.com/4ysJFMe.jpg', 'images/go-cubs-2.jpg'),
    ('https://i.imgur.com/CGMgkfg.jpg', 'images/fishing-trip-in-nc.jpg'),
    ('https://i.imgur.com/mKngwyF.jpg', 'images/first-time-in-times-square.jpg'),
    ('https://i.imgur.com/GJyV92t.jpg', 'images/first-waymo-ride-in-sf.jpg'),
    ('https://i.imgur.com/59kkPmw.jpg', 'images/hot-air-balloon-festival-in-the-traverse-city-area.jpg'),
    ('https://i.imgur.com/ktU5bfO.jpg', 'images/seeing-darryl-from-the-office-at-comedy-cellar.jpg'),
    ('https://i.imgur.com/24R9mlC.jpg', 'images/one-of-the-coolest-dinners-ever-at-abra-ovata-in-athens.jpg'),
    ('https://i.imgur.com/l8lVeX8.jpg', 'images/skybar-lounge-in-mykonos.jpg'),
    ('https://i.imgur.com/BmKEh3v.jpg', 'images/birthday-bowling-in-croatia.jpg'),
    ('https://i.imgur.com/jId7qsw.jpg', 'images/boat-day-in-traverse-city.jpg'),
    ('https://i.imgur.com/KpWCqzR.jpg', 'images/proposing-to-my-life-partner.jpg'),
    ('https://i.imgur.com/tLwnT3o.jpg', 'images/clubbing-in-spain-after-we-got-engaged.jpg'),
    ('https://i.imgur.com/OVC1uCY.jpg', 'images/kayaking-in-spain.jpg'),
    ('https://i.imgur.com/idaDkpA.jpg', 'images/monastery-hike-at-montserrat.jpg'),
    ('https://i.imgur.com/Erzd1KL.jpg', 'images/chilling-in-front-of-the-eiffel-tower.jpg'),
    ('https://i.imgur.com/Qoa6B3f.jpg', 'images/skydiving-in-switzerland.jpg'),
    ('https://i.imgur.com/0rDs7lP.jpg', 'images/hot-tubbing-in-iceland.jpg'),
    ('https://i.imgur.com/BilusmU.jpg', 'images/bubbles-in-iceland.jpg'),
    ('https://i.imgur.com/QIbbn30.jpg', 'images/puzzles-and-wine-in-iceland.jpg'),
    ('https://i.imgur.com/bXQTQKc.png', 'images/jumping-into-the-arctic-harbor-in-tromso-at-4-degrees-c.png'),
    ('https://i.imgur.com/QKWSrDF.jpeg', 'images/seeing-the-northern-lights-in-tromso.jpeg'),
    ('https://i.imgur.com/dcpNbto.jpeg', 'images/feeding-reindeer-in-the-wild.jpeg'),
    ('https://i.imgur.com/IM5kkvp.jpg', 'images/gainsight-conference-in-amsterdam.jpg'),
    ('https://i.imgur.com/bWbrS1k.jpg', 'images/ring-road-in-iceland.jpg'),
    ('https://i.imgur.com/pGneGKO.jpg', 'images/brother-and-sister-in-law-getting-married.jpg'),
    ('https://i.imgur.com/mGyb9PB.jpg', 'images/monkey-hike-in-thailand.jpg'),
    ('https://i.imgur.com/itahIt4.jpg', 'images/lantern-festival-in-chiang-mai.jpg'),
    ('https://i.imgur.com/uDktqG7.jpg', 'images/rainbow-hike.jpg'),
    ('https://i.imgur.com/4fiNUNd.jpg', 'images/floating-market-in-thailand.jpg'),
    ('https://i.imgur.com/HXBnV0s.png', 'images/the-devil-s-wheel-at-oktoberfest.png'),
    ('https://i.imgur.com/9xEvWAU.jpg', 'images/skiing-in-cortina-d-ampezzo.jpg'),
    ('https://i.imgur.com/zobgNu9.jpg', 'images/surfing-in-portugal.jpg'),
    ('https://i.imgur.com/A2gq4z2.jpg', 'images/bioluminescent-plankton-swim-at-night-in-krabi.jpg'),
    ('https://i.imgur.com/swyN3Ws.jpg', 'images/trevi-fountain-in-the-middle-of-the-night.jpg'),
    ('https://i.imgur.com/eikSHiK.jpg', 'images/paella-class-in-barcelona.jpg'),
    ('https://gcdnb.pbrd.co/images/iwItbdFZLzI6.jpg?o=1', 'images/in-the-hospital-after-the-marathon.jpg'),
    ('https://i.imgur.com/T9UiUwI.jpg', 'images/function-health-biological-age.jpg'),
]


def fetch(url, dest):
    req = Request(url, headers={"User-Agent": UA, "Referer": "https://samfarber.com/"})
    with urlopen(req, timeout=30) as r:
        data = r.read()
        ctype = r.headers.get("content-type", "")
    if not ctype.startswith("image/"):
        raise RuntimeError(f"non-image content-type: {ctype}")
    with open(dest, "wb") as f:
        f.write(data)
    return len(data), ctype


def main():
    os.makedirs("images", exist_ok=True)
    ok = skipped = failed = 0
    failures = []
    for i, (url, dest) in enumerate(MAPPING, 1):
        prefix = f"[{i:2d}/{len(MAPPING)}]"
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f"{prefix} SKIP {dest}", flush=True)
            skipped += 1
            continue
        try:
            size, ctype = fetch(url, dest)
            print(f"{prefix} OK   {dest}  ({size} bytes, {ctype})", flush=True)
            ok += 1
        except Exception as e:
            print(f"{prefix} FAIL {dest}  {type(e).__name__}: {e}", flush=True)
            failed += 1
            failures.append((url, dest, f"{type(e).__name__}: {e}"))
            if os.path.exists(dest):
                os.remove(dest)
        time.sleep(0.1)

    print(f"\nDone. ok={ok} skipped={skipped} failed={failed}")
    if failures:
        with open("images/_failures.txt", "w") as f:
            for url, dest, err in failures:
                f.write(f"{dest}\t{url}\t{err}\n")
        print(f"\n{failed} failures written to images/_failures.txt")
    # Always exit 0 so the workflow commits whatever images succeeded.


if __name__ == "__main__":
    main()
