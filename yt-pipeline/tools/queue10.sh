#!/bin/bash
cd /tmp/claude-0/-home-user-testhub/bb4ef4fc-c670-5f4a-bf57-6ec4d730ed34/scratchpad
export NOWAIT=1
for x in "$@"; do set -- $x; ./daily.sh $1 $2 v10; done
echo QUEUE DONE
