"""Forlænger Instagram-adgangsnøglen (gyldig i 60 dage ad gangen).

Køres månedligt af .github/workflows/forny-noegle.yml. Skriver den nye nøgle
til filen i $NY_NOEGLE_FIL, så workflowet kan gemme den som hemmeligheden IG_TOKEN.
Nøglen skrives aldrig til loggen.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

token = os.environ.get("IG_TOKEN", "").strip()
out = os.environ.get("NY_NOEGLE_FIL")
if not token or not out:
    print("Mangler IG_TOKEN eller NY_NOEGLE_FIL.")
    sys.exit(1)

url = "https://graph.instagram.com/refresh_access_token?" + urllib.parse.urlencode(
    {"grant_type": "ig_refresh_token", "access_token": token}
)
try:
    with urllib.request.urlopen(url, timeout=60) as r:
        data = json.loads(r.read().decode())
except urllib.error.HTTPError as e:
    print(f"Fornyelse fejlede ({e.code}). Opret en ny nøgle, se OPSÆTNING.md.")
    sys.exit(1)

new = data.get("access_token")
if not new:
    print("Svaret indeholdt ingen nøgle.")
    sys.exit(1)
print(f"::add-mask::{new}")
with open(out, "w") as fh:
    fh.write(new)
days = int(data.get("expires_in", 0)) // 86400
print(f"Nøglen er fornyet og gælder i ca. {days} dage.")
