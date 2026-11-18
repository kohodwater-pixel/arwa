/* HIPPO franchise enquiry — three steps, validation and submission. No dependencies. */
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
      age_bad: "تحقّق من العمر المكتوب.",
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
      age_bad: "Check the age you entered.",
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
  var LAST = 3;
  var stepEls = {}, alerts = {};
  [1, 2, 3].forEach(function (n) {
    stepEls[n] = document.getElementById("step-" + n);
    alerts[n] = document.getElementById("alert-" + n);
  });
  var backBtns = form.querySelectorAll("[data-prev]");
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

  // ---------- this tab's session: answers survive the language switch; one id per enquiry ----------
  var STORE = "hippo-franchise-enquiry";
  var KEEP = ["full_name", "profession", "age", "company_name", "company_website", "mobile", "email",
    "experience", "experience_other", "own_brand", "branches_operated", "why_hippo",
    "branches_wanted", "branches_wanted_other", "investment_source", "investment_source_other",
    "investment_amount", "start_time", "target_cities", "has_location", "heard_from", "notes"];
  function newId() {
    return (window.crypto && crypto.randomUUID) ? crypto.randomUUID()
      : Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 12);
  }
  var session = { id: newId(), step: 1, values: {} };
  try {
    var saved = JSON.parse(sessionStorage.getItem(STORE) || "null");
    if (saved && saved.id && saved.values) session = saved;
  } catch (e) { /* storage unavailable: the form still works, it just does not remember */ }

  function isRadio(name) { return f[name] && !f[name].tagName; } // a RadioNodeList has no tagName
  function remember() {
    KEEP.forEach(function (name) { session.values[name] = isRadio(name) ? picked(name) : f[name].value; });
    session.step = current;
    try { sessionStorage.setItem(STORE, JSON.stringify(session)); } catch (e) { /* ignore */ }
  }
  function forget() {
    session = { id: newId(), step: 1, values: {} };
    try { sessionStorage.removeItem(STORE); } catch (e) { /* ignore */ }
  }

  // ---------- rules: one entry per checked field, in page order ----------
  var RULES = [
    { name: "full_name", step: 1, check: need(T.full_name) },
    { name: "profession", step: 1, check: need(T.profession) },
    { name: "age", step: 1, check: function (v) {
        v = cleanNumber(v);
        if (!/^\d{1,3}$/.test(v)) return T.age_empty;
        if (Number(v) < 18) return T.age_min;
        return Number(v) <= 120 ? "" : T.age_bad;
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
    { name: "branches_wanted", step: 3, group: true, check: choice("branches_wanted") },
    { name: "branches_wanted_other", step: 3, check: otherOf("branches_wanted") },
    { name: "investment_source", step: 3, group: true, check: choice("investment_source") },
    { name: "investment_source_other", step: 3, check: otherOf("investment_source") },
    { name: "investment_amount", step: 3, check: function (v) {
        if (!v) return T.amount_empty;
        v = cleanNumber(v);
        return /^\d{1,15}(\.\d{1,2})?$/.test(v) && Number(v) > 0 ? "" : T.amount_bad;
      } },
    { name: "start_time", step: 3, group: true, check: choice("start_time") },
    { name: "target_cities", step: 3, check: need(T.target_cities) },
    { name: "consent", step: 3, box: true, check: function () { return f.consent.checked ? "" : T.consent; } }
  ];

  function errEl(rule) { return document.getElementById(rule.name + "-error"); }

  function validate(rule) {
    var msg = rule.check(rule.group || rule.box ? "" : val(rule.name));
    var err = errEl(rule);
    err.textContent = msg;
    err.hidden = !msg;
    if (rule.group) {
      document.getElementById(rule.name + "-group").classList.toggle("invalid", !!msg);
      var rg = document.getElementById(rule.name + "-choices");
      if (msg) rg.setAttribute("aria-invalid", "true"); else rg.removeAttribute("aria-invalid");
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

  form.addEventListener("input", remember);
  form.addEventListener("change", remember);

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
    [1, 2, 3].forEach(function (i) { stepEls[i].hidden = i !== n; });
    stepsBox.setAttribute("data-step", String(n));
    document.getElementById("step-now").textContent = String(n);
    stepName.textContent = stepName.getAttribute("data-s" + n);
    remember();
    if (focus !== false) {
      stepsText.focus({ preventScroll: true });
      document.getElementById("form-title").scrollIntoView({ block: "start" });
    }
  }

  Array.prototype.forEach.call(form.querySelectorAll("[data-next]"), function (btn) {
    btn.addEventListener("click", function () { if (validateStep(current)) goTo(current + 1); });
  });
  Array.prototype.forEach.call(backBtns, function (btn) {
    btn.addEventListener("click", function () { goTo(current - 1); });
  });
  // Pressing a step button must not first blur the field being edited: the blur check could
  // insert an error line, move the button under the pointer and swallow the click.
  Array.prototype.forEach.call(form.querySelectorAll(".actions button"), function (btn) {
    btn.addEventListener("mousedown", function (e) { e.preventDefault(); });
  });

  // Enter in a text field of an earlier step moves on instead of submitting the hidden last step.
  form.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.target.tagName === "INPUT" && current < LAST) {
      e.preventDefault();
      if (validateStep(current)) goTo(current + 1);
    }
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
    // The answer as the visitor read it (page language), next to the stable code.
    RADIOS.forEach(function (name) {
      var el = form.querySelector('input[name="' + name + '"]:checked');
      d[name + "_label"] = el ? el.parentNode.textContent.trim() : "";
    });
    d.heard_from_label = d.heard_from ? f.heard_from.options[f.heard_from.selectedIndex].textContent.trim() : "";
    d.consent = "yes";
    d.submission_id = session.id;
    // Spam trap: sent as it is, never judged here. The receiving side files flagged rows separately,
    // so a real applicant whose autofill touched the hidden field is not lost.
    d.trap = f.f_check.value;
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
    Array.prototype.forEach.call(backBtns, function (b) { b.disabled = busy; });
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
    // Give up after a fixed wait so the visitor is never left on "sending".
    var timer = null;
    if (window.AbortController) {
      var ctl = new AbortController();
      opts.signal = ctl.signal;
      timer = setTimeout(function () { ctl.abort(); }, Number(cfg.SEND_TIMEOUT_MS) || 25000);
    }
    function done(x) { clearTimeout(timer); return x; }
    return fetch(endpoint, opts).then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.text();
    }).then(done, function (err) { done(); throw err; }).then(function (body) {
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
    if (current < LAST) { if (validateStep(current)) goTo(current + 1); return; }
    if (!validateStep(LAST)) return;
    // Earlier steps were checked on "next"; check again in case they were edited after going back.
    for (var n = 1; n < LAST; n++) {
      var bad = RULES.filter(function (r) { return r.step === n && r.check(r.group ? "" : val(r.name)); });
      if (bad.length) { goTo(n, false); validateStep(n); return; }
    }

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
      forget(); // stored answers are cleared and the next enquiry gets a new id
      finish("live");
    }).catch(function () {
      setBusy(false);
      sendFailed = true;
      alerts[LAST].textContent = T.send_failed;
      alerts[LAST].hidden = false;
      alerts[LAST].focus();
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

  // ---------- restore what this tab already holds (e.g. after switching language) ----------
  KEEP.forEach(function (name) {
    var v = session.values[name];
    if (!v) return;
    if (isRadio(name)) {
      var el = form.querySelector('input[name="' + name + '"][value="' + String(v).replace(/[^a-z0-9\-]/gi, "") + '"]');
      if (el) el.checked = true;
    } else {
      f[name].value = v;
    }
  });
  ["experience", "branches_wanted", "investment_source"].forEach(function (name) {
    document.getElementById(name + "_other-wrap").hidden = picked(name) !== "other";
  });
  if (session.step > 1 && session.step <= LAST) {
    current = session.step;
    [1, 2, 3].forEach(function (i) { stepEls[i].hidden = i !== current; });
    stepsBox.setAttribute("data-step", String(current));
    document.getElementById("step-now").textContent = String(current);
    stepName.textContent = stepName.getAttribute("data-s" + current);
  }
})();
