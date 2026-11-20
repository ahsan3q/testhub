#!/bin/bash
cd /tmp/claude-0/-home-user-testhub/bb4ef4fc-c670-5f4a-bf57-6ec4d730ed34/scratchpad
# wait while another worker/daily render is active
while pgrep -f "worker10[.]sh" >/dev/null || pgrep -f "daily[.]sh p0" >/dev/null; do sleep 30; done
for v in "$@"; do ./worker.sh $v 2>&1 | grep -E "FINISHED|FAIL|DONE"; done
