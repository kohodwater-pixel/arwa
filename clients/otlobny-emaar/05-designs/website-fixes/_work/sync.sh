#!/bin/bash
# copies the v02 files into the test server layout (index.php at root, assets/css, assets/js)
D="$(cd "$(dirname "$0")" && pwd)"; V="$D/../otlobny-emaar_website-fixes_phase1_ar_v03"
cp "$V/index.php" "$D/serve/index.php"; cp "$V/site.css" "$D/serve/assets/css/site.css"; cp "$V/site.js" "$D/serve/assets/js/site.js"; cp "$V/sitemap.xml" "$D/serve/sitemap.xml"
