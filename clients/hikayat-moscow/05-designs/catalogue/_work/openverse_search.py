"""Query Openverse for open-licence photos of each hotel / city. ~1 request per 3 s, stops on 429."""
import json, time, urllib.request, urllib.parse, pathlib, sys
OUT = pathlib.Path(__file__).parent / "openverse"
QUERIES = {
 "st-regis": ["St. Regis Moscow Nikolskaya", "St Regis Nikolskaya"],
 "garden-plaza": ["Garden Plaza hotel Moscow"],
 "ararat": ["Ararat Park Hyatt Moscow", "Ararat Park Hotel Moscow"],
 "cosmos-arbat": ["Cosmos Arbat hotel Moscow"],
 "intercontinental": ["InterContinental Moscow Tverskaya"],
 "marriott": ["Marriott Royal Aurora Moscow"],
 "safmar": ["Safmar Grand Moscow"],
 "national": ["Hotel National Moscow"],
 "brosko": ["Brosko hotel Moscow Arbat"],
 "cosmos-nevsky": ["Cosmos Royal Nevsky Saint Petersburg"],
 "corinthia": ["Corinthia Hotel Saint Petersburg", "Corinthia Nevsky Palace"],
 "city-moscow": ["Moscow Kremlin skyline"],
 "city-spb": ["Saint Petersburg Neva embankment"],
}
for key, qs in QUERIES.items():
    for q in qs:
        url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "cc0,pdm,by,by-sa", "page_size": 20})
        req = urllib.request.Request(url, headers={"User-Agent": "catalogue-image-check/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            print(key, q, "HTTP", e.code); 
            if e.code == 429: sys.exit(0)
            time.sleep(3); continue
        except Exception as e:
            print(key, q, "ERR", e); time.sleep(3); continue
        (OUT / f"{key}__{q.replace(' ','_').replace('.','')}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
        print(key, q, data.get("result_count"), len(data.get("results", [])))
        time.sleep(3.2)
