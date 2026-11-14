# Spanish faceless YouTube pipeline

Retro documentary-style videos (teal textured background, clips in cards / vintage TV frame, yellow labels,
bold captions, countdown reveals, keyframed map / counter / timeline / quote / compare / list graphics,
whoosh SFX, generated music bed) narrated in Spanish with Edge neural voices.

## Workflow per video
1. Pick competitor's top video (vidIQ `channel_videos popular=true`) → get transcript (`video_transcript`).
2. Verify facts (`tools/wiki.py`, Wikipedia REST with browser UA) — fix competitor mistakes.
3. Write `projects/<name>/script.json` (Spanish, own wording). Segment fields:
   `src` (key in sources.json or `MIX`), `label` (must match the footage shown), `cap` (`#N` = countdown reveal),
   `txt` (narration), optional `fx` ({type: map|counter|timeline|quote|compare|list, ..., dur}).
4. Footage: `tools/ia.py "<archive.org query>"` then `tools/iadl.py <identifier> src` → `sources.json`.
   Crop/trim watermarks, timecodes and end cards before use. Every shot ≤ 3.8 s.
5. Voice: `tools/vo.py <project> <voice> <rate>` (aim ~150–155 wpm).
6. `tools/assets.py tools/assets <music_seconds>` once, then `tools/build.py <project> <project>/sources.json`.
7. `meta.json` → `tools/meta.py <project>` (title / description with chapters / tags / script txt).
8. Thumbnail in competitor layout (translated text, real archive frames — no AI likenesses of real people).
9. `tools/finish.sh <project> <drive_folder_id> vNN` → compress + upload via Apps Script (`apps_script_drive_upload.gs`).

## Requirements
ffmpeg, python3 (pillow, numpy), `pip install edge-tts yt-dlp rembg[cpu]`; edge-tts needs `--proxy "$HTTPS_PROXY"` in the cloud env.
`tools/.env` (not committed): `DRIVE_UPLOAD_URL=https://script.google.com/macros/s/.../exec`

## Channels (Drive: YT-Automation/YouTube Spanish Channels)
| # | Model channel | v01 |
|---|---|---|
| 01 | Drollery | Lee Marvin war stories |
| 02 | Sovrenza | Hollywood legends on Bruce Lee |
| 03 | Retro Secrets Vault | Short-lived cartoons of 1940 |
| 04 | The Toon Attic | Betty Boop 10 facts |
| 05 | America's Golden Days | 7 controversial commercials |
| 06 | Hungerwise | Most embarrassing food failures |

Target from v02: 15+ minutes, clips matched to each segment's subject.
