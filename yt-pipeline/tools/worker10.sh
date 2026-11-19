#!/bin/bash
# renders v10 projects as they become ready (script, meta, thumb, FOLDER, .dl_ok); exits when all 6 finished
cd /tmp/claude-0/-home-user-testhub/bb4ef4fc-c670-5f4a-bf57-6ec4d730ed34/scratchpad
export NOWAIT=1
declare -A V=([01]=es-US-AlonsoNeural [02]=es-MX-JorgeNeural [03]=es-MX-JorgeNeural [04]=es-MX-DaliaNeural [05]=es-US-AlonsoNeural [06]=es-CO-GonzaloNeural)
while true; do
  left=0; did=0
  for c in 02 04 03 01 05 06; do
    P=p${c}v10; grep -q "FINISHED v10" $P/finish3.log 2>/dev/null && continue; left=1
    [ -f $P/.dl_ok ] && [ -s $P/script.json ] && [ -s $P/meta.json ] && [ -s $P/thumb/v01_thumbnail.jpg ] && [ -s $P/FOLDER ] || continue
    ./daily.sh $P ${V[$c]} v10; did=1; break
  done
  [ $left = 0 ] && { echo ALL V10 DONE; break; }
  [ $did = 0 ] && sleep 60
done
