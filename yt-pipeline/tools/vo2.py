"""VO v2: edge-tts audio + per-word timings (for karaoke subtitles).
usage: vo2.py <project_dir> <voice> <rate>
writes vo/NN.mp3 and vo/NN.json  ([{"w": word, "s": start_sec, "e": end_sec}, ...])
"""
import asyncio, json, os, sys, subprocess
import edge_tts

P, VOICE, RATE = sys.argv[1], sys.argv[2], sys.argv[3]
seg = json.load(open(f"{P}/script.json")); os.makedirs(f"{P}/vo", exist_ok=True)
PROXY = os.environ.get("HTTPS_PROXY")
os.environ.setdefault("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt")

async def one(i, sem):
    async with sem:
        mp3, js = f"{P}/vo/{i:02d}.mp3", f"{P}/vo/{i:02d}.json"
        for attempt in range(5):
            try:
                c = edge_tts.Communicate(seg[i]["txt"], VOICE, rate=RATE, boundary="WordBoundary", proxy=PROXY)
                words, audio = [], bytearray()
                async for ch in c.stream():
                    if ch["type"] == "audio": audio += ch["data"]
                    elif ch["type"] == "WordBoundary":
                        s = ch["offset"] / 1e7; e = s + ch["duration"] / 1e7
                        words.append({"w": ch["text"], "s": round(s, 3), "e": round(e, 3)})
                if len(audio) > 1000 and words:
                    open(mp3, "wb").write(audio); json.dump(words, open(js, "w"), ensure_ascii=False)
                    return True
            except Exception as ex:
                err = ex
            await asyncio.sleep(2 + attempt * 2)
        print("FAIL", i, err); return False

async def main():
    sem = asyncio.Semaphore(4)
    await asyncio.gather(*[one(i, sem) for i in range(len(seg))])
asyncio.run(main())
tot = sum(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{P}/vo/{i:02d}.mp3"])) for i in range(len(seg)))
w = sum(len(s["txt"].split()) for s in seg); print("segs", len(seg), "sec", round(tot), "wpm", round(w / tot * 60))
