/* HIPPO franchise enquiry — connection settings.
   This is the ONLY file to edit when the form is connected. See ../../README.md.

   While FORM_ENDPOINT and WHATSAPP_NUMBER are both empty, the page stays in
   DRAFT mode: it validates, sends nothing, and says so on screen. */
window.HIPPO_FORM_CONFIG = {
  // Where the enquiry is sent. Empty = not connected.
  // Google Sheet: paste the web-app URL that ends in /exec
  // (it starts with https://script.google.com/). Nothing else needs changing.
  FORM_ENDPOINT: "",

  // Only for endpoints that are NOT Google Apps Script:
  // "json" (application/json), "form" (application/x-www-form-urlencoded)
  // or "text" (JSON sent as text/plain, no CORS preflight).
  FORM_FORMAT: "json",

  // Simple alternative with no server: international number, digits only, no "+".
  // Used only when FORM_ENDPOINT is empty. The visitor's WhatsApp opens with the
  // enquiry written out; they press send themselves.
  WHATSAPP_NUMBER: "",

  // Privacy notice links. While empty, the page shows a marked "to be supplied" note.
  PRIVACY_URL_AR: "",
  PRIVACY_URL_EN: ""
};
