#!/usr/bin/env python3
"""Writes hedaya-nouman_cv_content_ar-en_v02.md from the same source as the designed files."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_cv as B

M = B.MODELS
head = """# Hedaya Nouman — CV content (Arabic + English), v02 DRAFT

**Status:** v02 draft, not approved. Supersedes v01 (now in `_archive/`).
**Sources:** `01-brief/brief.md` only — the original CV, the client's first message, and the section "Client answers — 2026-11-16", which overrides the earlier assumptions. Nothing else was added.
**Single source:** this copy is generated from `06-profiles/cv/_work/build_cv.py`, the same data that produces the DOCX, the ATS PDFs and the Executive PDFs, so the wording below is exactly what is in the 12 designed files.
**Conventions:** Western numerals in both languages; Arabic punctuation in Arabic; feminine forms throughout the Arabic; no first-person pronouns in English; no birth year, marital status, photo or hobbies; no city printed for employers; no figures, because the client gave none.
**Dates:** Arabic `يونيو 2022 إلى ديسمبر 2026`, `2016 إلى 2017`, `2015`; English `Jun 2022 – Dec 2026`, `2016 – 2017`, `2015`.

## What changed from v01

- Hospital role rewritten around the client's confirmed facts: hospitality (hotel) services and room services in the hospital, leading the work team, training new female employees, the hospital information system and Microsoft Excel. The title «أخصائية خدمة عملاء» is kept and the scope is stated beside it.
- School role: title is now «منسقة إدارية» / Administrative Coordinator; the guidance bullets are withdrawn.
- Added: nationality, the year 2020 on all four courses, a Technical Skills section, and competencies she can now claim (team leadership, new staff training, hospitality services in healthcare, room services).
- Hospitality model is no longer written as a career change: it states four-plus years of hospitality and room services in a hospital setting and a target role in the hospitality sector. No hotel employment or hotel system is claimed. "Guest Relations" is removed.
- Review r1: Arabic date ranges use «إلى»; complaints are "recorded and referred", not resolved; "Patient & Visitor Service" replaces "Patient & Visitor Experience"; competency sets are identical in both languages; "certificate of appreciation", "pilgrims (Duyuf Al-Rahman)" and «بوصفه» are used consistently; "Brings a warm welcome" and "busy service environments" are gone.

| Model | Headline | Section order (ATS) |
|---|---|---|
| CS | Customer Service Specialist — أخصائية خدمة عملاء | Summary, Competencies, Technical Skills, Experience, Education, Training, Volunteering, Languages |
| HS | Customer Service Specialist – Hospitality & Room Services, with "Target Role: Hospitality Services Specialist" on the next line | Summary, Competencies, Technical Skills, Experience, Volunteering, Training, Education, Languages |

In the Executive Modern layout the same content sits in two zones: side column (contact, technical skills, education, training, languages) and main column (summary, competencies, experience, volunteering). There the contact details are shown as four captioned items instead of two lines.

---
"""
titles = {("cs", "ar"): "## 1. Model CS — Arabic (أخصائية خدمة عملاء)",
          ("cs", "en"): "## 2. Model CS — English (Customer Service Specialist)",
          ("hs", "ar"): "## 3. Model HS — Arabic (الخدمات الفندقية)",
          ("hs", "en"): "## 4. Model HS — English (Hospitality Services)"}
body = ""
for k in [("cs", "ar"), ("cs", "en"), ("hs", "ar"), ("hs", "en")]:
    body += titles[k] + "\n\n" + B.md_cv(M[k]).rstrip() + "\n\n---\n\n"

ca, ce = M[("cs", "ar")], M[("cs", "en")]
A, En = B.AR, B.EN


def pair(a, e):
    return f"- [ ] {a}  \n      {e}\n"


tail = f"""## 5. Lines to confirm with the client

Much shorter than in v01: the hospital role now rests on the client's own answers. What is left is wording that goes one step beyond what she said, and the two older roles, for which only the job title is known.

### 5.1 Hospital role — wording that goes slightly beyond the confirmed facts

Confirmed by the client: hospitality and room services in the hospital; led the work team; trained new female employees; used the hospital information system and Microsoft Excel. The bullets are the same in both models (order differs).

{pair(ca["hospital"][0], ce["hospital"][0])}      Confirm that the team she led was the hospitality and room-services team (the two facts were given separately).
{pair(ca["hospital"][3], ce["hospital"][3])}      "To patients" is inferred; she said only where she worked. Add companions or visitors if that is accurate.
{pair(ca["hospital"][2], ce["hospital"][2])}      Inferred from the job title «أخصائية خدمة عملاء», not from her answers. Worded as recording and referring, not resolving.
- [ ] **Role title line** «{A["hospital"][0]}» / "{En["hospital"][0]}": the scope is added beside the original title. The exact official title is still to be confirmed.

Not listed for confirmation because they restate her answers directly: «{ca["hospital"][1]}» and «{ca["hospital"][4]}» (and their English lines).

### 5.2 Earlier roles — bullets inferred from the job title only

**{En["school"][0]} — {En["school"][1]} ({En["school"][2]})**

{pair(A["school_bullets"][0], En["school_bullets"][0])}{pair(A["school_bullets"][1], En["school_bullets"][1])}
**{En["reception"][0]} — {En["reception"][1]} ({En["reception"][2]})**

{pair(A["reception_bullets"][0], En["reception_bullets"][0])}{pair(A["reception_bullets"][1], En["reception_bullets"][1])}      "Patients" in the English line is inferred from the employer being a medical group.

### 5.3 Derived wording and keywords

- [ ] **"More than four years" / «تزيد على أربع سنوات»** is calculated from Jun 2022 – Dec 2026.
- [ ] **End date December 2026** is printed on the client's instruction; on 16 Nov 2026 it is still in the future, and the English bullets are in the past tense. Say whether "Present" / «حتى الآن» should be used until she has left.
- [ ] **Competencies that rest on job titles, not on a statement from her:** Enquiry Handling, Complaint Handling, Front Desk & Reception, Administrative Coordination, Communication Skills, Patient & Visitor Service; in the hospitality model also Guest Services, Guest Reception & Welcome and Service Etiquette (offered as competencies from serving patients as guests, not as hotel duties).
- [ ] **"Training new staff"** in the English summaries stands for "trained new female employees"; the bullet keeps her exact wording.

### 5.4 Still open

- [ ] **English names of organisations and courses** are translations, not confirmed official names (hospital, medical group, school, IPA course titles, the secretarial certificate, "Consultation Point" Programme, the two social development committees, Madinah Charitable Diabetes Society). "Duyuf Al-Rahman" is a transliteration of «ضيوف الرحمن».
- [ ] **Pilgrim volunteering location** is not stated, so no city is printed. If it was in Madinah, adding it strengthens the hospitality model.
- [ ] **«نقطة استشارة» hours** are printed as listed (32 hours, and a certificate for 16 hours); whether the 16 are part of the 32 is unknown, so no total is given.
- [ ] **Issuer of the secretarial certificate** is unknown and not printed.
- [ ] **Availability** is not printed (default in the brief). No LinkedIn exists, so none is shown.
- [ ] **Team size, numbers served, results:** none given, none printed. One real figure would strengthen every version.

### 5.5 Confirmed since v01 (no longer open)

Name spelling Hedaya Fakhri Nouman; English level Basic; nationality Saudi; school job title Administrative Coordinator; all four courses taken in 2020; hospital scope, team leadership, training and systems as above.
"""
(B.OUT / f"hedaya-nouman_cv_content_ar-en_{B.V}.md").write_text(head + body + tail, encoding="utf-8")
print("content written")
