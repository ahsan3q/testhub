#!/bin/bash
# usage: runq.sh <project> <folderId> <vNN> : serialized render+upload (flock), waits for any unlocked build too
S=/tmp/claude-0/-home-user-testhub/bb4ef4fc-c670-5f4a-bf57-6ec4d730ed34/scratchpad; P=$S/$1
exec 9>$S/render.lock; flock 9
while pgrep -f "python3 -I ../tools/build.py" >/dev/null || pgrep -f "tools/finish.sh" >/dev/null; do sleep 30; done
cd $P && python3 -I ../tools/build.py . sources.json > build_log.txt 2>&1
grep -q '^done' build_log.txt && $S/tools/finish.sh $P $2 $3 > finish_log.txt 2>&1
echo "$1: $(grep FINISHED finish_log.txt 2>/dev/null || tail -2 build_log.txt)"
