/**
 * HIPPO franchise enquiry → Google Sheet.
 *
 * Paste this whole file into the Apps Script editor that is opened FROM the
 * spreadsheet (Extensions › Apps Script), then deploy it as a web app:
 *   Execute as: Me      Who has access: Anyone
 * Each enquiry sent by the form becomes one row in the "Enquiries" tab.
 * Rows that tripped the form's hidden spam trap go to a "Spam" tab instead,
 * so nothing is thrown away and a real applicant can still be found there.
 *
 * NOT TESTED against a live Google account by the agency: it was written and
 * reviewed by reading only. Send a test enquiry after deploying (see README).
 */

var SHEET_NAME = 'Enquiries';
var SPAM_SHEET_NAME = 'Spam';
var FORM_ID = 'hippo-franchise-enquiry';

// Column order after the timestamp. Keep it stable: add new fields at the END,
// and add the matching title to row 1 of the tab by hand (see ensureHeader).
// "*_label" columns hold the answer as the visitor read it, in the page language;
// the column before each holds the stable internal code.
var FIELDS = [
  'full_name', 'profession', 'age', 'company_name', 'company_website', 'mobile', 'email',
  'experience', 'experience_label', 'experience_other', 'own_brand', 'branches_operated', 'why_hippo',
  'branches_wanted', 'branches_wanted_label', 'branches_wanted_other',
  'investment_source', 'investment_source_label', 'investment_source_other',
  'investment_amount', 'investment_currency',
  'start_time', 'start_time_label', 'target_cities',
  'has_location', 'has_location_label', 'heard_from', 'heard_from_label', 'notes',
  'consent', 'lang', 'submission_id'
];
var HEADER = ['timestamp'].concat(FIELDS);
var ID_COLUMN = HEADER.indexOf('submission_id') + 1;

var LONG_FIELDS = { why_hippo: 1500, notes: 1500 }; // characters
var DEFAULT_LIMIT = 300;
var MAX_BODY = 20000;   // characters; anything larger is refused
var DEDUPE_ROWS = 50;   // a repeated submission_id within the last rows is not stored twice

function doPost(e) {
  try {
    var raw = (e && e.postData && e.postData.contents) || '';
    if (!raw || raw.length > MAX_BODY) return reply({ ok: false, error: 'bad request' });

    var data;
    try { data = JSON.parse(raw); } catch (err) { data = (e && e.parameter) || {}; }
    if (!data || data.form !== FORM_ID) return reply({ ok: false, error: 'unknown form' });

    // The hidden trap field: real visitors leave it empty. A filled trap is filed
    // in the Spam tab without further checks; it is never silently dropped.
    var flagged = clean(data.trap, DEFAULT_LIMIT) !== '';

    if (!flagged) {
      if (!clean(data.full_name, DEFAULT_LIMIT) || !clean(data.mobile, DEFAULT_LIMIT)) {
        return reply({ ok: false, error: 'missing required fields' });
      }
      if (data.consent !== 'yes') return reply({ ok: false, error: 'consent missing' });
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(clean(data.email, DEFAULT_LIMIT))) {
        return reply({ ok: false, error: 'invalid email' });
      }
    }

    var row = [new Date()];
    for (var i = 0; i < FIELDS.length; i++) {
      var name = FIELDS[i];
      row.push(clean(data[name], LONG_FIELDS[name] || DEFAULT_LIMIT));
    }
    var id = clean(data.submission_id, DEFAULT_LIMIT);

    var lock = LockService.getScriptLock();
    lock.waitLock(20000); // two enquiries at the same moment must not share a row
    try {
      var book = SpreadsheetApp.getActiveSpreadsheet();
      var tab = flagged ? SPAM_SHEET_NAME : SHEET_NAME;
      var sheet = book.getSheetByName(tab) || book.insertSheet(tab);
      ensureHeader(sheet);

      // A retry of the same enquiry (same id) is answered "ok" without a second row.
      var last = sheet.getLastRow();
      if (id && last > 1) {
        var count = Math.min(DEDUPE_ROWS, last - 1);
        var recent = sheet.getRange(last - count + 1, ID_COLUMN, count, 1).getValues();
        for (var r = 0; r < recent.length; r++) {
          if (String(recent[r][0]) === id) return reply({ ok: true, duplicate: true });
        }
      }

      // Formats first, values second: column A is a date, everything else plain text
      // (keeps the leading 0 or + of phone numbers and stops numbers being reformatted).
      var target = sheet.getRange(last + 1, 1, 1, row.length);
      target.setNumberFormat('@');
      target.getCell(1, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
      target.setValues([row]);
      SpreadsheetApp.flush();
    } finally {
      lock.releaseLock();
    }
    return reply({ ok: true });
  } catch (err) {
    return reply({ ok: false, error: 'server error' });
  }
}

// The title row is written ONLY when the tab is completely empty. If you add,
// remove or reorder columns in FIELDS later, an existing tab keeps its old titles:
// fix row 1 by hand, or start a new tab.
function ensureHeader(sheet) {
  if (sheet.getLastRow() === 0) {
    sheet.appendRow(HEADER);
    sheet.setFrozenRows(1);
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
