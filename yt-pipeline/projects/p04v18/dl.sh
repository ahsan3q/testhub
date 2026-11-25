#!/bin/bash
cd /tmp/claude-0/-home-user-testhub/bb4ef4fc-c670-5f4a-bf57-6ec4d730ed34/scratchpad/p04v18
get(){ k=$1; u=$2; [ -s src/$k.mp4 ] || curl -sL --retry 3 -o src/$k.mp4 "$u"; echo "$k|src/$k.mp4 $(( $(stat -c %s src/$k.mp4)/1048576 )) MB" >> dl_log.txt; echo "$k ok"; }
: > dl_log.txt
get FG "https://archive.org/download/TheFriendlyGhost/TheFriendlyGhost_512kb.mp4"
get GB "https://archive.org/download/noveltoon_casper_tfg_theres_good_boos_tonight/noveltoon_casper_tfg_theres_good_boos_tonight_512kb.mp4"
get HW "https://archive.org/download/CasperTheFriendlyGhostTheater/3.AHauntingWeWillGo1949.mp4"
C="https://archive.org/download/casper-the-friendly-ghost-the-complete-collection-1950-59"
get BM "$C/Casper%20-%20Boo%20Moon%20%281954%29.mp4"
get BS "$C/Casper%20-%20Boo%20Scout%20%281951%29.mp4"
get BP "$C/Casper%20-%20Casper%27s%20Birthday%20Party%20%281959%29.mp4"
get CC "$C/Casper%20-%20Casper%20Comes%20to%20Clown%20%281951%29.mp4"
echo ALLDL
