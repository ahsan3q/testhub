#!/bin/bash
# usage: finish.sh <project_dir> <drive_folder_id> <vNN>
set -e
P="$1"; FID="$2"; V="$3"; T=$(dirname "$0")
ffmpeg -y -hide_banner -loglevel error -i "$P/final.mp4" -c:v libx264 -preset faster -crf 24 -maxrate 6M -bufsize 12M -pix_fmt yuv420p -c:a copy -movflags +faststart "$P/upload/$V.mp4"
"$T/drive_upload.sh" "$P/upload/$V.mp4" "$FID" "$V.mp4" video/mp4
"$T/drive_upload.sh" "$P/thumb/v01_thumbnail.jpg" "$FID" "${V}_thumbnail.jpg" image/jpeg
for f in titulo descripcion tags guion; do "$T/drive_upload.sh" "$P/upload/$f.txt" "$FID" "${V}_$f.txt" text/plain; done
echo "FINISHED $V $(du -h "$P/upload/$V.mp4" | cut -f1)"
# free disk after successful upload
rm -f "${P:?}/final.mp4" "${P:?}/build/video.mp4" "${P:?}/build/audio.m4a" "${P:?}/upload/${V:?}.mp4"
rm -rf "${P:?}/build/shots"
