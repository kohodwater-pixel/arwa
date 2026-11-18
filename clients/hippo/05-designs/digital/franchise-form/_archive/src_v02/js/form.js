/* HIPPO franchise enquiry — two steps, validation and submission. No dependencies. */
(function () {
  "use strict";

  var cfg = window.HIPPO_FORM_CONFIG || {};
  var lang = document.documentElement.lang === "en" ? "en" : "ar";

  var T = {
    ar: {
      full_name: "اكتب اسمك الكامل.",
      profession: "اكتب مهنتك.",
      age_empty: "اكتب عمرك بالأرقام.",
      age_min: "يجب ألا يقل العمر عن 18 سنة.",
      website_bad: "تحقّق من عنوان الموقع.",
      mobile_empty: "اكتب رقم جوالك.",
      mobile_bad: "الرقم غير مكتمل. اكتبه بالأرقام فقط، ويمكن أن يبدأ بمفتاح الدولة.",
      email_empty: "اكتب بريدك الإلكتروني.",
      email_bad: "تحقّق من صيغة البريد الإلكتروني.",
      choose: "اختر إجابة واحدة.",
      other: "اكتب إجابتك هنا.",
      number_bad: "اكتب العدد بالأرقام فقط.",
      why_hippo: "اكتب لنا سبب اهتمامك بامتياز هيبو.",
      amount_empty: "اكتب المبلغ الذي تنوي استثماره.",
      amount_bad: "اكتب المبلغ بالأرقام فقط.",
      target_cities: "اكتب المدن التي تستهدفها.",
      consent: "نحتاج موافقتك حتى نتواصل معك.",
      summary_one: "حقل واحد يحتاج تصحيحًا.",
      summary_many: "بعض الحقول تحتاج تصحيحًا. راجع الملاحظات تحت كل حقل.",
      sending: "جارٍ الإرسال…",
      send_failed: "تعذّر الإرسال. بياناتك ما زالت في النموذج؛ تحقّق من الاتصال وحاول مرة أخرى.",
      privacy_link: "إشعار الخصوصية",
      wa_title: "استفسار عن امتياز هيبو التجاري"
    },
    en: {
      full_name: "Enter your full name.",
      profession: "Enter your profession.",
      age_empty: "Enter your age in digits.",
      age_min: "Applicants must be 18 or older.",
      website_bad: "Check the website address.",
      mobile_empty: "Enter your mobile number.",
      mobile_bad: "That number looks incomplete. Use digits only; it can start with a country code.",
      email_empty: "Enter your email address.",
      email_bad: "Check the email address format.",
      choose: "Choose one answer.",
      other: "Write your answer here.",
      number_bad: "Use digits only.",
      why_hippo: "Tell us why the HIPPO franchise interests you.",
      amount_empty: "Enter the amount you plan to invest.",
      amount_bad: "Enter the amount in digits only.",
      target_cities: "Enter the cities you're targeting.",
      consent: "We need your consent before we can contact you.",
      summary_one: "One field needs a correction.",
      summary_many: "Some fields need a correction. See the note under each one.",
      sending: "Sending…",
      send_failed: "We couldn't send it. Your answers are still in the form; check your connection and try again.",
      privacy_link: "Privacy notice",
      wa_title: "HIPPO franchise enquiry"
    }
  }[lang];

  var endpoint = (cfg.FORM_ENDPOINT || "").trim();
  var whatsapp = String(cfg.WHATSAPP_NUMBER || "").replace(/\D/g, "");
  var mode = endpoint ? "live" : whatsapp ? "whatsapp" : "draft";
  // A Google Apps Script web app only accepts a cross-origin POST without a
  // preflight, so it is sent as text/plain and must answer {"ok": true}.
  var isAppsScript = /^https:\/\/script\.google\.com\//.test(endpoint);
  var format = isAppsScript ? "text" : (cfg.FORM_FORMAT || "json");

  var form = document.getElementById("enquiry-form");
  var f = form.elements;
  var formPanel = document.getElementById("form-panel");
  var stepEls = { 1: document.getElementById("step-1"), 2: document.getElementById("step-2") };
  var alerts = { 1: document.getElementById("alert-1"), 2: document.getElementById("alert-2") };
  var stepsBox = document.getElementById("steps");
  var stepsText = document.getElementById("steps-text");
  var stepName = document.getElementById("step-name");
  var submitBtn = document.getElementById("submit-btn");
  var submitLabel = submitBtn.textContent;
  var panels = {
    live: document.getElementById("done-live"),
    whatsapp: document.getElementById("done-whatsapp"),
    draft: document.getElementById("done-draft")
  };
  var current = 1;
  var sendFailed = false;

  // The draft strip is in the HTML by default and is removed only when connected.
  if (mode !== "draft") document.getElementById("draft-strip").hidden = true;

  // Privacy notice: real link when supplied, marked gap otherwise.
  var privacyUrl = ((lang === "en" ? cfg.PRIVACY_URL_EN : cfg.PRIVACY_URL_AR) || "").trim();
  if (privacyUrl) {
    var slot = document.getElementById("privacy-slot");
    var a = document.createElement("a");
    a.href = privacyUrl;
    a.target = "_blank";
    a.rel = "noopener";
    a.textContent = T.privacy_link;
    slot.textContent = "";
    slot.appendChild(a);
  }

  // ---------- helpers ----------
  // Arabic-Indic and Persian digits are accepted and stored as Western digits.
  function western(s) {
    return s.replace(/[٠-٩]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); })
            .replace(/[۰-۹]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); });
  }
  function cleanPhone(s) { return western(s).replace(/[\s\-().]/g, ""); }
  function cleanNumber(s) { return western(s).replace(/[\s,،٬]/g, ""); }
  function val(name) { return f[name].value.trim(); }
  function picked(name) {
    var el = form.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : "";
  }
  function need(msg) { return function (v) { return v.length >= 2 ? "" : msg; }; }
  function choice(name) { return function () { return picked(name) ? "" : T.choose; }; }
  function otherOf(name) { return function (v) { return picked(name) !== "other" || v.length >= 2 ? "" : T.other; }; }

  // ---------- rules: one entry per checked field, in page order ----------
  var RULES = [
    { name: "full_name", step: 1, check: need(T.full_name) },
    { name: "profession", step: 1, check: need(T.profession) },
    { name: "age", step: 1, check: function (v) {
        v = cleanNumber(v);
        if (!/^\d{1,3}$/.test(v)) return T.age_empty;
        return Number(v) >= 18 && Number(v) <= 120 ? "" : (Number(v) < 18 ? T.age_min : T.age_empty);
      } },
    { name: "company_website", step: 1, check: function (v) {
        return !v || /^(https?:\/\/)?[^\s\/.]+(\.[^\s\/.]+)+(\/\S*)?$/i.test(v) ? "" : T.website_bad;
      } },
    { name: "mobile", step: 1, check: function (v) {
        if (!v) return T.mobile_empty;
        return /^(\+|00)?\d{8,15}$/.test(cleanPhone(v)) ? "" : T.mobile_bad;
      } },
    { name: "email", step: 1, check: function (v) {
        if (!v) return T.email_empty;
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? "" : T.email_bad;
      } },
    { name: "experience", step: 2, group: true, check: choice("experience") },
    { name: "experience_other", step: 2, check: otherOf("experience") },
    { name: "branches_operated", step: 2, check: function (v) { return !v || /^\d{1,5}$/.test(cleanNumber(v)) ? "" : T.number_bad; } },
    { name: "why_hippo", step: 2, check: need(T.why_hippo) },
    { name: "branches_wanted", step: 2, group: true, check: choice("branches_wanted") },
    { name: "branches_wanted_other", step: 2, check: otherOf("branches_wanted") },
    { name: "investment_source", step: 2, group: true, check: choice("investment_source") },
    { name: "investment_source_other", step: 2, check: otherOf("investment_source") },
    { name: "investment_amount", step: 2, check: function (v) {
        if (!v) return T.amount_empty;
        v = cleanNumber(v);
        return /^\d{1,15}(\.\d{1,2})?$/.test(v) && Number(v) > 0 ? "" : T.amount_bad;
      } },
    { name: "start_time", step: 2, group: true, check: choice("start_time") },
    { name: "target_cities", step: 2, check: need(T.target_cities) },
    { name: "consent", step: 2, box: true, check: function () { return f.consent.checked ? "" : T.consent; } }
  ];

  function errEl(rule) { return document.getElementById(rule.name + "-error"); }

  function validate(rule) {
    var msg = rule.check(rule.group || rule.box ? "" : val(rule.name));
    var err = errEl(rule);
    err.textContent = msg;
    err.hidden = !msg;
    if (rule.group) {
      document.getElementById(rule.name + "-group").classList.toggle("invalid", !!msg);
    } else if (msg) {
      f[rule.name].setAttribute("aria-invalid", "true");
    } else {
      f[rule.name].removeAttribute("aria-invalid");
    }
    // The summary above the buttons goes away once nothing in the step is left to correct.
    if (!msg && !sendFailed && !stepEls[rule.step].querySelector(".error:not([hidden])")) alerts[rule.step].hidden = true;
    return !msg;
  }

  function firstControl(rule) {
    return rule.group ? form.querySelector('input[name="' + rule.name + '"]') : f[rule.name];
  }

  function validateStep(n) {
    var bad = RULES.filter(function (r) { return r.step === n; }).filter(function (r) { return !validate(r); });
    if (!bad.length) { alerts[n].hidden = true; return true; }
    alerts[n].textContent = bad.length === 1 ? T.summary_one : T.summary_many;
    alerts[n].hidden = false;
    firstControl(bad[0]).focus();
    return false;
  }

  // Check a field when the visitor leaves it; once it shows an error, re-check as they type.
  RULES.forEach(function (rule) {
    var nodes = rule.group ? form.querySelectorAll('input[name="' + rule.name + '"]') : [f[rule.name]];
    Array.prototype.forEach.call(nodes, function (el) {
      var isChoice = el.type === "radio" || el.type === "checkbox";
      if (!isChoice) el.addEventListener("blur", function () { if (el.value.trim() || el.hasAttribute("aria-invalid")) validate(rule); });
      el.addEventListener(isChoice ? "change" : "input", function () { if (!errEl(rule).hidden) validate(rule); });
    });
  });

  // "Other" reveals a required text field under the question.
  ["experience", "branches_wanted", "investment_source"].forEach(function (name) {
    var wrap = document.getElementById(name + "_other-wrap");
    var otherRule = RULES.filter(function (r) { return r.name === name + "_other"; })[0];
    Array.prototype.forEach.call(form.querySelectorAll('input[name="' + name + '"]'), function (radio) {
      radio.addEventListener("change", function () {
        var on = picked(name) === "other";
        wrap.hidden = !on;
        if (!on) validate(otherRule); // clears a stale error
      });
    });
  });

  // ---------- steps ----------
  function goTo(n, focus) {
    current = n;
    stepEls[1].hidden = n !== 1;
    stepEls[2].hidden = n !== 2;
    stepsBox.setAttribute("data-step", String(n));
    document.getElementById("step-now").textContent = String(n);
    stepName.textContent = stepName.getAttribute("data-s" + n);
    if (focus !== false) {
      stepsText.focus({ preventScroll: true });
      document.getElementById("form-title").scrollIntoView({ block: "start" });
    }
  }

  document.getElementById("next-btn").addEventListener("click", function () { if (validateStep(1)) goTo(2); });
  document.getElementById("back-btn").addEventListener("click", function () { goTo(1); });
  // Enter in a step-1 field moves on instead of submitting the hidden second step.
  stepEls[1].addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target.tagName === "INPUT") { e.preventDefault(); if (validateStep(1)) goTo(2); }
  });

  // ---------- data ----------
  var ORDER = ["full_name", "profession", "age", "company_name", "company_website", "mobile", "email",
    "experience", "experience_other", "own_brand", "branches_operated", "why_hippo",
    "branches_wanted", "branches_wanted_other", "investment_source", "investment_source_other",
    "investment_amount", "investment_currency", "start_time", "target_cities", "has_location", "heard_from", "notes"];
  var RADIOS = ["experience", "branches_wanted", "investment_source", "start_time", "has_location"];

  function payload() {
    var d = { form: "hippo-franchise-enquiry", lang: lang };
    ORDER.forEach(function (name) {
      if (name === "investment_currency") d[name] = "SAR";
      else if (RADIOS.indexOf(name) > -1) d[name] = picked(name);
      else if (/_other$/.test(name)) d[name] = picked(name.replace(/_other$/, "")) === "other" ? val(name) : "";
      else d[name] = val(name);
    });
    d.age = cleanNumber(d.age);
    d.mobile = cleanPhone(d.mobile);
    d.branches_operated = cleanNumber(d.branches_operated);
    d.investment_amount = cleanNumber(d.investment_amount);
    d.consent = "yes";
    d.submitted_at = new Date().toISOString();
    return d;
  }

  // The enquiry as the visitor sees it (labels and chosen answers), for the WhatsApp text.
  function readable(d) {
    var lines = [T.wa_title];
    ORDER.forEach(function (name) {
      if (!d[name] || name === "investment_currency") return;
      var label, value = d[name];
      if (RADIOS.indexOf(name) > -1) {
        label = document.querySelector("#" + name + "-group legend").firstChild.textContent.trim();
        value = form.querySelector('input[name="' + name + '"]:checked').parentNode.textContent.trim();
        if (d[name] === "other") return; // the written answer follows on its own line
      } else if (/_other$/.test(name)) {
        label = document.querySelector("#" + name.replace(/_other$/, "") + "-group legend").firstChild.textContent.trim();
      } else {
        label = document.querySelector('label[for="' + name + '"]').firstChild.textContent.trim();
        if (name === "heard_from") value = f.heard_from.options[f.heard_from.selectedIndex].textContent.trim();
        if (name === "investment_amount") value += " SAR";
      }
      lines.push(label + ": " + value);
    });
    return lines.join("\n");
  }

  // ---------- sending ----------
  function finish(which) {
    formPanel.hidden = true;
    panels[which].hidden = false;
    panels[which].focus({ preventScroll: true });
    panels[which].scrollIntoView({ block: "start" });
  }

  function setBusy(busy) {
    submitBtn.disabled = busy;
    document.getElementById("back-btn").disabled = busy;
    submitBtn.textContent = busy ? T.sending : submitLabel;
    form.setAttribute("aria-busy", busy ? "true" : "false");
  }

  function send(data) {
    var opts = { method: "POST", headers: {} };
    if (format === "form") {
      opts.body = new URLSearchParams(data);
    } else if (format === "text") {
      opts.headers["Content-Type"] = "text/plain;charset=utf-8";
      opts.body = JSON.stringify(data);
    } else {
      opts.headers["Content-Type"] = "application/json";
      opts.headers.Accept = "application/json";
      opts.body = JSON.stringify(data);
    }
    return fetch(endpoint, opts).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.text();
    }).then(function (body) {
      var reply = null;
      try { reply = JSON.parse(body); } catch (e) { /* not JSON */ }
      // Apps Script answers 200 even for its own error pages, so only an explicit
      // {"ok": true} from our script counts as stored. Other endpoints: 2xx is success
      // unless they say {"ok": false}.
      if (isAppsScript ? !(reply && reply.ok === true) : (reply && reply.ok === false)) throw new Error("not confirmed");
    });
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    sendFailed = false;
    if (current === 1) { if (validateStep(1)) goTo(2); return; }
    if (!validateStep(2)) return;
    // Step 1 was checked on "next"; check again in case it was edited after going back.
    var step1Bad = RULES.filter(function (r) { return r.step === 1 && r.check(val(r.name)); });
    if (step1Bad.length) { goTo(1, false); validateStep(1); return; }

    // Honeypot: a filled trap field means a bot. Show the ordinary end state, send nothing.
    if (f.hp_field.value) { finish(mode); return; }

    var data = payload();
    if (mode === "draft") { finish("draft"); return; }
    if (mode === "whatsapp") {
      window.open("https://wa.me/" + whatsapp + "?text=" + encodeURIComponent(readable(data)), "_blank", "noopener");
      finish("whatsapp");
      return;
    }

    setBusy(true);
    send(data).then(function () {
      setBusy(false);
      finish("live");
    }).catch(function () {
      setBusy(false);
      sendFailed = true;
      alerts[2].textContent = T.send_failed;
      alerts[2].hidden = false;
      alerts[2].focus();
    });
  });

  // "Back to the form" on the draft and WhatsApp panels (answers are kept).
  Array.prototype.forEach.call(document.querySelectorAll("[data-back]"), function (btn) {
    btn.addEventListener("click", function () {
      Object.keys(panels).forEach(function (k) { panels[k].hidden = true; });
      formPanel.hidden = false;
      goTo(current);
    });
  });
})();
