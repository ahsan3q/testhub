#!/bin/bash
# usage: daily.sh <proj> <voice> <vNN>   (resumable). Finishes once thumb/v01_thumbnail.jpg, meta.json and FOLDER exist.
S=/tmp/claude-0/-home-user-testhub/bb4ef4fc-c670-5f4a-bf57-6ec4d730ed34/scratchpad
P=$S/$1; cd "$P" || exit 1
grep -q "FINISHED $3" finish3.log 2>/dev/null && { echo "$1: already done"; exit 0; }
mkdir -p src upload
[ -f .dl_ok ] || { $S/redl.sh "$P" > redl.log 2>&1 && touch .dl_ok; }
NS=$(python3 -c "import json;print(len(json.load(open('script.json'))))"); NJ=$(ls vo/*.json 2>/dev/null | wc -l)
if [ "$NJ" != "$NS" ]; then
  for r in -6 -10 -13 -16 -19 -22; do
    rm -rf vo; python3 -I $S/tools/vo2.py . "$2" "${r}%" > vo2.log 2>&1
    sec=$(grep -o 'sec [0-9]*' vo2.log | awk '{print $2}')
    [ "${sec:-0}" -ge 885 ] && break
  done
fi
if [ ! -s final.mp4 ]; then
  for try in 1 2; do JOBS=${JOBS:-2} flock $S/render.lock python3 -u -I $S/tools/build3.py . sources.json >> build3.log 2>&1; rc=$?; echo "build rc=$rc" >> build_rc.log; [ -s final.mp4 ] && break; done; [ -s final.mp4 ] || { echo "$1 BUILD FAIL rc=$rc"; grep -v -E "Deprecation|cov = " build3.log | tail -8; exit 1; }
fi
if [ -n "$NOWAIT" ] && ! { [ -s thumb/v01_thumbnail.jpg ] && [ -s meta.json ] && [ -s FOLDER ]; }; then echo "$1: built, waiting for thumb/meta"; exit 0; fi
until [ -s thumb/v01_thumbnail.jpg ] && [ -s meta.json ] && [ -s FOLDER ]; do sleep 20; done
python3 -I $S/tools/meta.py . > /dev/null
$S/tools/finish.sh "$P" "$(cat FOLDER)" "$3" > finish3.log 2>&1
grep -q FINISHED finish3.log && rm -rf "${P:?}/build3" "${P:?}/src"
echo "$1: $(tail -1 finish3.log)"
