#!/bin/bash
# usage: drive_upload.sh <file> <parentFolderId> [name] [mime]
set -e
[ -f "$(dirname "$0")/.env" ] && . "$(dirname "$0")/.env"
F="$1"; P="$2"; N="${3:-$(basename "$F")}"; M="${4:-video/mp4}"
URL="${DRIVE_UPLOAD_URL:?set DRIVE_UPLOAD_URL (Apps Script web app URL) in env or tools/.env}"
S=$(stat -c %s "$F")
J=$(curl -sS -L --max-time 120 -H "Content-Type: application/json" -d "{\"name\":\"$N\",\"parentId\":\"$P\",\"mimeType\":\"$M\",\"size\":$S}" "$URL")
L=$(python3 -c "import json,sys;print(json.loads(sys.argv[1])['location'])" "$J")
curl -sS --max-time 3600 -X PUT -H "Content-Type: $M" --upload-file "$F" "$L" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('id'),d.get('name'))"
