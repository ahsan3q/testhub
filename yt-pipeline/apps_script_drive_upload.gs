// Google Apps Script web app: creates a resumable Drive upload session inside ROOT folder only.
// Deploy: Execute as "Me", access "Anyone". Put the /exec URL in tools/.env as DRIVE_UPLOAD_URL=...
const ROOT = 'PUT_YT_AUTOMATION_FOLDER_ID_HERE';
function doPost(e) {
  try {
    const p = JSON.parse(e.postData.contents);
    if (!insideRoot_(p.parentId)) return out_({ error: 'folder not allowed' });
    const r = UrlFetchApp.fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable', {
      method: 'post', contentType: 'application/json; charset=UTF-8',
      payload: JSON.stringify({ name: p.name, parents: [p.parentId], mimeType: p.mimeType }),
      headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken(), 'X-Upload-Content-Type': p.mimeType, 'X-Upload-Content-Length': String(p.size) },
      muteHttpExceptions: true });
    const h = r.getHeaders();
    return out_({ code: r.getResponseCode(), location: h['Location'] || h['location'] || null, body: r.getContentText().slice(0, 800) });
  } catch (err) { return out_({ error: String(err) }); }
}
function insideRoot_(id) {
  let f = DriveApp.getFolderById(id);
  for (let i = 0; i < 10; i++) { if (f.getId() === ROOT) return true; const ps = f.getParents(); if (!ps.hasNext()) return false; f = ps.next(); }
  return false;
}
function out_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function scopeHelper_() { DriveApp.createFile('x', 'y'); }  // run once to grant Drive write scope
