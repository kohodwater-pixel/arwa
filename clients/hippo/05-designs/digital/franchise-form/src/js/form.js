/* HIPPO franchise enquiry — validation and submission. No dependencies. */
(function () {
  "use strict";

  var cfg = window.HIPPO_FORM_CONFIG || {};
  var lang = document.documentElement.lang === "en" ? "en" : "ar";

  var T = {
    ar: {
      name: "اكتب اسمك الكامل.",
      mobile_empty: "اكتب رقم جوالك.",
      mobile_bad: "الرقم غير مكتمل. اكتبه بالأرقام فقط، ويمكن أن يبدأ بمفتاح الدولة.",
      email_bad: "تحقّق من صيغة البريد الإلكتروني.",
      city: "اكتب المدينة أو المنطقة التي تريد الافتتاح فيها.",
      has_location: "اختر إجابة واحدة.",
      consent: "نحتاج موافقتك حتى نتواصل معك.",
      summary_one: "حقل واحد يحتاج تصحيحًا.",
      summary_many: "بعض الحقول تحتاج تصحيحًا. راجع الملاحظات تحت كل حقل.",
      sending: "جارٍ الإرسال…",
      send_failed: "تعذّر الإرسال. بياناتك ما زالت في النموذج؛ تحقّق من الاتصال وحاول مرة أخرى.",
      privacy_link: "إشعار الخصوصية",
      wa_title: "استفسار عن امتياز هيبو التجاري",
      labels: { full_name: "الاسم", mobile: "الجوال", email: "البريد", city: "المدينة أو المنطقة", has_location: "الموقع", experience: "الخبرة", heard_from: "كيف سمعت عنا", message: "الرسالة" }
    },
    en: {
      name: "Enter your full name.",
      mobile_empty: "Enter your mobile number.",
      mobile_bad: "That number looks incomplete. Use digits only; it can start with a country code.",
      email_bad: "Check the email address format.",
      city: "Enter the city or region where you want to open.",
      has_location: "Choose one answer.",
      consent: "We need your consent before we can contact you.",
      summary_one: "One field needs a correction.",
      summary_many: "Some fields need a correction. See the note under each one.",
      sending: "Sending…",
      send_failed: "We couldn't send it. Your answers are still in the form; check your connection and try again.",
      privacy_link: "Privacy notice",
      wa_title: "HIPPO franchise enquiry",
      labels: { full_name: "Name", mobile: "Mobile", email: "Email", city: "City or region", has_location: "Location", experience: "Experience", heard_from: "Heard from", message: "Message" }
    }
  }[lang];

  var endpoint = (cfg.FORM_ENDPOINT || "").trim();
  var whatsapp = String(cfg.WHATSAPP_NUMBER || "").replace(/\D/g, "");
  var mode = endpoint ? "live" : whatsapp ? "whatsapp" : "draft";

  var form = document.getElementById("enquiry-form");
  var formPanel = document.getElementById("form-panel");
  var summary = document.getElementById("form-alert");
  var submitBtn = document.getElementById("submit-btn");
  var submitLabel = submitBtn.textContent;
  var panels = {
    live: document.getElementById("done-live"),
    whatsapp: document.getElementById("done-whatsapp"),
    draft: document.getElementById("done-draft")
  };

  // The draft strip is in the HTML by default and is removed only when connected.
  if (mode !== "draft") {
    var strip = document.getElementById("draft-strip");
    if (strip) strip.hidden = true;
  }

  // Privacy notice: real link when supplied, marked gap otherwise.
  var privacyUrl = (lang === "en" ? cfg.PRIVACY_URL_EN : cfg.PRIVACY_URL_AR) || "";
  if (privacyUrl.trim()) {
    var slot = document.getElementById("privacy-slot");
    var a = document.createElement("a");
    a.href = privacyUrl.trim();
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = T.privacy_link;
    slot.textContent = "";
    slot.appendChild(a);
  }

  // Arabic-Indic and Persian digits are accepted and stored as Western digits.
  function westernDigits(s) {
    return s.replace(/[٠-٩]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); })
            .replace(/[۰-۹]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); });
  }
  function cleanPhone(s) { return westernDigits(s).replace(/[\s\-().]/g, ""); }

  var checks = {
    full_name: function (v) { return v.trim().length >= 2 ? "" : T.name; },
    mobile: function (v) {
      if (!v.trim()) return T.mobile_empty;
      return /^(\+|00)?\d{8,15}$/.test(cleanPhone(v)) ? "" : T.mobile_bad;
    },
    email: function (v) {
      if (!v.trim()) return "";
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : T.email_bad;
    },
    city: function (v) { return v.trim().length >= 2 ? "" : T.city; },
    has_location: function () { return form.querySelector('input[name="has_location"]:checked') ? "" : T.has_location; },
    consent: function () { return form.elements.consent.checked ? "" : T.consent; }
  };
  var order = ["full_name", "mobile", "email", "city", "has_location", "consent"];

  function show(name, msg) {
    var err = document.getElementById(name + "-error");
    err.textContent = msg;
    err.hidden = !msg;
    if (name === "has_location") {
      document.getElementById("has_location-group").classList.toggle("invalid", !!msg);
      return;
    }
    var el = form.elements[name];
    if (msg) el.setAttribute("aria-invalid", "true"); else el.removeAttribute("aria-invalid");
  }

  function validate(name) {
    var el = form.elements[name];
    var msg = checks[name](el && el.value !== undefined ? el.value : "");
    show(name, msg);
    // The summary above the button goes away once nothing is left to correct.
    if (!msg && !form.querySelector(".error:not([hidden])") && !form.hasAttribute("data-send-failed")) summary.hidden = true;
    return !msg;
  }

  // Check a field when the visitor leaves it; once it has an error, re-check as they type.
  order.forEach(function (name) {
    var nodes = name === "has_location" ? form.querySelectorAll('input[name="has_location"]') : [form.elements[name]];
    Array.prototype.forEach.call(nodes, function (el) {
      var isChoice = el.type === "radio" || el.type === "checkbox";
      if (!isChoice) el.addEventListener("blur", function () { if (el.value.trim() || el.hasAttribute("aria-invalid")) validate(name); });
      el.addEventListener(isChoice ? "change" : "input", function () {
        if (!document.getElementById(name + "-error").hidden) validate(name);
      });
    });
  });

  function payload() {
    var f = form.elements;
    var loc = form.querySelector('input[name="has_location"]:checked');
    return {
      form: "hippo-franchise-enquiry",
      lang: lang,
      full_name: f.full_name.value.trim(),
      mobile: cleanPhone(f.mobile.value),
      email: f.email.value.trim(),
      city: f.city.value.trim(),
      has_location: loc ? loc.value : "",
      experience: f.experience.value.trim(),
      heard_from: f.heard_from.value,
      message: f.message.value.trim(),
      consent: "yes",
      submitted_at: new Date().toISOString()
    };
  }

  function visibleText(name, data) {
    if (name === "has_location") {
      var loc = form.querySelector('input[name="has_location"]:checked');
      return loc ? loc.parentNode.textContent.trim() : "";
    }
    if (name === "heard_from") {
      var s = form.elements.heard_from;
      return s.value ? s.options[s.selectedIndex].textContent.trim() : "";
    }
    return data[name];
  }

  function finish(which) {
    formPanel.hidden = true;
    var p = panels[which];
    p.hidden = false;
    p.focus();
    p.scrollIntoView({ block: "start" });
  }

  function setBusy(busy) {
    submitBtn.disabled = busy;
    submitBtn.textContent = busy ? T.sending : submitLabel;
    form.setAttribute("aria-busy", busy ? "true" : "false");
  }

  function send(data) {
    var opts = { method: "POST", headers: { Accept: "application/json" } };
    if ((cfg.FORM_FORMAT || "json") === "form") {
      opts.body = new URLSearchParams(data);
    } else {
      opts.headers["Content-Type"] = "application/json";
      opts.body = JSON.stringify(data);
    }
    return fetch(endpoint, opts).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    summary.hidden = true;
    form.removeAttribute("data-send-failed");

    var bad = order.filter(function (name) { return !validate(name); });
    if (bad.length) {
      summary.textContent = bad.length === 1 ? T.summary_one : T.summary_many;
      summary.hidden = false;
      var first = bad[0] === "has_location" ? form.querySelector('input[name="has_location"]') : form.elements[bad[0]];
      first.focus();
      return;
    }

    // Honeypot: a filled trap field means a bot. Show the ordinary end state, send nothing.
    if (form.elements.company_website.value) { finish(mode); return; }

    var data = payload();

    if (mode === "draft") { finish("draft"); return; }

    if (mode === "whatsapp") {
      var lines = [T.wa_title];
      Object.keys(T.labels).forEach(function (k) {
        var v = visibleText(k, data);
        if (v) lines.push(T.labels[k] + ": " + v);
      });
      window.open("https://wa.me/" + whatsapp + "?text=" + encodeURIComponent(lines.join("\n")), "_blank", "noopener");
      finish("whatsapp");
      return;
    }

    setBusy(true);
    send(data).then(function () {
      setBusy(false);
      finish("live");
    }).catch(function () {
      setBusy(false);
      form.setAttribute("data-send-failed", "");
      summary.textContent = T.send_failed;
      summary.hidden = false;
      summary.focus();
    });
  });

  // "Back to the form" on the draft and WhatsApp panels (answers are kept).
  Array.prototype.forEach.call(document.querySelectorAll("[data-back]"), function (btn) {
    btn.addEventListener("click", function () {
      Object.keys(panels).forEach(function (k) { panels[k].hidden = true; });
      formPanel.hidden = false;
      document.getElementById("form-title").focus();
    });
  });
})();
