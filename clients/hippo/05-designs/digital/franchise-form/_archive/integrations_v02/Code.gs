/**
 * HIPPO franchise enquiry → Google Sheet.
 *
 * Paste this whole file into the Apps Script editor that is opened FROM the
 * spreadsheet (Extensions › Apps Script), then deploy it as a web app:
 *   Execute as: Me      Who has access: Anyone
 * Each enquiry sent by the form becomes one row in the tab named below.
 *
 * NOT TESTED against a live Google account by the agency: it was written and
 * reviewed by reading only. Send a test enquiry after deploying (see README).
 */

var SHEET_NAME = 'Enquiries';
var FORM_ID = 'hippo-franchise-enquiry';

// Column order. Keep it stable: new fields are added at the end.
var FIELDS = [
  'full_name', 'profession', 'age', 'company_name', 'company_website', 'mobile', 'email',
  'experience', 'experience_other', 'own_brand', 'branches_operated', 'why_hippo',
  'branches_wanted', 'branches_wanted_other', 'investment_source', 'investment_source_other',
  'investment_amount', 'investment_currency', 'start_time', 'target_cities',
  'has_location', 'heard_from', 'notes', 'consent', 'lang'
];
var HEADER = ['timestamp'].concat(FIELDS);

var LONG_FIELDS = { why_hippo: 1500, notes: 1500 }; // characters
var DEFAULT_LIMIT = 300;
var MAX_BODY = 20000; // characters; anything larger is refused

function doPost(e) {
  try {
    var raw = (e && e.postData && e.postData.contents) || '';
    if (!raw || raw.length > MAX_BODY) return reply({ ok: false, error: 'bad request' });

    var data;
    try { data = JSON.parse(raw); } catch (err) { data = (e && e.parameter) || {}; }
    if (!data || data.form !== FORM_ID) return reply({ ok: false, error: 'unknown form' });

    // Spam trap: real visitors never see this field. Answer "ok" and store nothing.
    if (data.hp_field) return reply({ ok: true });

    if (!clean(data.full_name, DEFAULT_LIMIT) || !clean(data.mobile, DEFAULT_LIMIT)) {
      return reply({ ok: false, error: 'missing required fields' });
    }

    var row = [new Date()];
    for (var i = 0; i < FIELDS.length; i++) {
      var name = FIELDS[i];
      row.push(clean(data[name], LONG_FIELDS[name] || DEFAULT_LIMIT));
    }

    var lock = LockService.getScriptLock();
    lock.waitLock(20000); // two enquiries at the same moment must not share a row
    try {
      var book = SpreadsheetApp.getActiveSpreadsheet();
      var sheet = book.getSheetByName(SHEET_NAME) || book.insertSheet(SHEET_NAME);
      if (sheet.getLastRow() === 0) {
        sheet.appendRow(HEADER);
        sheet.setFrozenRows(1);
      }
      var target = sheet.getRange(sheet.getLastRow() + 1, 1, 1, row.length);
      target.setNumberFormat('@'); // plain text: keeps the leading 0 and + of phone numbers
      target.setValues([row]);
      target.getCell(1, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
      SpreadsheetApp.flush();
    } finally {
      lock.releaseLock();
    }
    return reply({ ok: true });
  } catch (err) {
    return reply({ ok: false, error: 'server error' });
  }
}

// Opening the /exec link in a browser shows this, which confirms the deployment is public.
function doGet() {
  return reply({ ok: true, service: FORM_ID, note: 'Endpoint is up. Enquiries are accepted by POST only.' });
}

// Text only, trimmed, length-limited, and never interpreted as a spreadsheet formula.
function clean(value, limit) {
  if (value === null || value === undefined) return '';
  var s = String(value).replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '').trim();
  if (s.length > limit) s = s.substring(0, limit);
  if (/^[=+\-@]/.test(s)) s = "'" + s;
  return s;
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
