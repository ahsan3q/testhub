#!/bin/bash
cd /tmp/claude-0/-home-user-testhub/bb4ef4fc-c670-5f4a-bf57-6ec4d730ed34/scratchpad
./redl.sh $PWD/p06v14 > p06v14/redl.log 2>&1
python3 -I tools/cimg.py p06v14/src S1 "Domino's Pizza store" S2 "Pizza Hut red roof restaurant" S3 "Pepsi cans" S4 "Coca-Cola bottles" S5 "Popeyes restaurant" S6 "Chick-fil-A restaurant" S7 "Krispy Kreme doughnuts" S8 "Dunkin Donuts store" S9 "McDonald's restaurant sign" S10 "Burger King restaurant" S11 "Red Bull can" S12 "Monster Energy can" S13 "Subway restaurant" S14 "Jersey Mike's Subs" S15 "In-N-Out Burger restaurant" S16 "Whataburger restaurant" > p06v14/cimg.log 2>&1
echo ALLDONE >> p06v14/cimg.log
