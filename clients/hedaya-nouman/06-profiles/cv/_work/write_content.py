#!/usr/bin/env python3
"""Writes hedaya-nouman_cv_content_ar-en_v01.md from the same source as the designed files."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_cv as B

M = B.MODELS
head = """# Hedaya Nouman — CV content (Arabic + English), v01 DRAFT

**Status:** v01 draft, not approved. Every fact comes from `01-brief/brief.md` (the original CV plus the client's message). Nothing else was added.
**Single source:** this copy is generated from `06-profiles/cv/_work/build_cv.py`, the same source that produces the DOCX, the ATS PDFs and the Executive PDFs, so the wording below is exactly what is in the 12 designed files.
**Conventions:** Western numerals in both languages; Arabic punctuation in Arabic; feminine forms throughout the Arabic; no first-person pronouns in English; no birth year, marital status, nationality, photo or hobbies; no city printed for employers.
**Date format:** `يونيو 2022 – ديسمبر 2026` / `Jun 2022 – Dec 2026`, `2016 – 2017`, `2015`.

Two models, each in two languages:

| Model | Target title | Section order |
|---|---|---|
| CS | Customer Service Specialist — أخصائية خدمة عملاء | Summary, Competencies, Experience, Education, Training, Volunteering, Languages |
| HS | Hospitality Services Specialist — أخصائية خدمات فندقية (career transition; no hotel employment claimed) | Summary, Competencies, Experience, Volunteering (pilgrim service first), Training, Education, Languages |

In the Executive Modern layout the same content is split into two zones: side column (contact, competencies, training, languages) and main column (summary, experience, then education and volunteering in the model's order).

---
"""
titles = {("cs", "ar"): "## 1. Model CS — Arabic (أخصائية خدمة عملاء)",
          ("cs", "en"): "## 2. Model CS — English (Customer Service Specialist)",
          ("hs", "ar"): "## 3. Model HS — Arabic (أخصائية خدمات فندقية)",
          ("hs", "en"): "## 4. Model HS — English (Hospitality Services Specialist)"}
body = ""
for k in [("cs", "ar"), ("cs", "en"), ("hs", "ar"), ("hs", "en")]:
    body += titles[k] + "\n\n" + B.md_cv(M[k]).rstrip() + "\n\n---\n\n"

def pairs(role):
    out = ""
    for mk in ("cs", "hs"):
        a, e = M[(mk, "ar")], M[(mk, "en")]
        la = a[role] if role in a else a["base"]["school_bullets"]
        le = e[role] if role in e else e["base"]["school_bullets"]
        for x, y in zip(la, le):
            tag = "CS + HS" if role == "school" else mk.upper()
            out += f"- [ ] ({tag}) {x}  \n      {y}\n"
        if role == "school":
            break
    return out

tail = f"""## 5. Lines to confirm with the client

The original CV gives job titles, employers and years only: no duties, no figures. Every experience bullet below is therefore **inferred from the job title** and must be confirmed, corrected or replaced by the client before any file is called final. Nothing here contains a number, a system name or a result.

### 5.1 Experience bullets inferred from the job title

**Customer Service Specialist — Dr. Hamed Sulaiman Al-Ahmadi Hospital (Jun 2022 – Dec 2026)**

{pairs("hospital")}
**Student guidance work — 92nd Primary School (2016 – 2017)** (same two bullets in both models)

{pairs("school")}
**Receptionist — Dr. Nizar Ibrahim Ghulam Medical Group (2015)**

{pairs("reception")}
### 5.2 Other inferred or derived wording

- [ ] **"More than four years" / «تزيد على أربع سنوات»** in both summaries is calculated from Jun 2022 – Dec 2026; it is not a figure the client gave.
- [ ] **End date December 2026** is printed on the client's instruction. On the day of writing (16 Nov 2026) that date is still in the future. English bullets for this role are written in the past tense; if she sends the CV before she leaves, a recruiter may ask about it. Confirm the date, and say whether "Present" should be used until she has actually left.
- [ ] **Summary qualities** — «وضوح التواصل» / "clear communication", «اللباقة» / "courteous service", «حسن الاستقبال» / "a warm welcome": not in the original's skills list (which has teamwork, adaptability, punctuality, computer skills, performing under pressure, self-development). They are stated as qualities, not achievements. Confirm she is comfortable with them.
- [ ] **Core competencies that are not in the original's skills list** and rest on the job titles and courses only: customer service, patient and visitor experience, enquiry handling, complaint handling, front desk and reception, communication skills, administrative support (from the secretarial certificate). HS only, listed as competencies she offers and not as past hotel duties: guest services, guest relations, guest reception and welcome, service etiquette.
- [ ] **"Patients" at the 2015 medical group** (English: "Greeted patients and visitors"; Arabic: «المراجعين والزوار») is inferred from the employer being a medical group.
- [ ] **«الطلبة» / "students"** in the school bullets: the original says only «العمل الإرشادي». Whether the work was with students, parents or both, and whether it was a girls' school, is unknown.

### 5.3 Assumptions

- [ ] **Name spelling in English:** Hedaya Fakhri Nouman, taken from the e-mail address. Confirm against the passport.
- [ ] **English level:** printed as «مستوى أساسي» / "Basic" (the original shows "40%"). Confirm the real level; it must not be raised without evidence.
- [ ] **Job title at the school:** printed as «العمل الإرشادي» / "Student Guidance Work" because the exact title is unknown. It reads as an activity, not a job title; the real title would be stronger.
- [ ] **HS headline:** «أخصائية خدمة ضيوف وعملاء | الهدف الوظيفي: أخصائية خدمات فندقية» / "Guest Services Professional | Target Role: Hospitality Services Specialist". The target role is labelled as a target so the line cannot be read as hotel employment.
- [ ] **Pilgrim volunteering location:** the original does not say where the 40 hours were served, so no city is printed next to it. If it was in Madinah, add «في المدينة المنورة» / "in Madinah" — it strengthens the HS model.
- [ ] **«نقطة استشارة» hours:** printed exactly as listed (32 volunteer hours, and a certificate of thanks for 16 hours). Whether the 16 hours are part of the 32 or additional is unknown, so no total is given anywhere.
- [ ] **Course wording:** the original's «القيادة الإدارة» is printed as «القيادة الإدارية». Course dates and hours are unknown and not printed. The issuer of the secretarial certificate is unknown and not printed.
- [ ] **English names of organisations** are translations, not confirmed official names: Dr. Hamed Sulaiman Al-Ahmadi Hospital; Dr. Nizar Ibrahim Ghulam Medical Group; 92nd Primary School; Institute of Public Administration (IPA) and its course titles "Developing Beneficiary (Customer) Services", "Time Management", "Administrative Leadership"; "Certificate in Principles of Administrative Secretarial Work"; "Consultation Point" Programme; Social Development Committee; Community Social Development Committee; Madinah Charitable Diabetes Society; World Diabetes Day Campaign 2018; World Kidney Day Activities.
- [ ] **Left out on purpose:** birth year, marital status, photo, hobbies, employer cities, and nationality (the original's «سعودية - المدينة المنورة» is ambiguous; add a nationality line only when confirmed, since it matters for Saudization-sensitive roles).

### 5.4 Still missing (asked in the brief, would strengthen every version)

- Actual duties at the hospital, and any numbers she can stand behind (visitors served per day, shift pattern, team size, complaints resolved).
- Systems or software used at work.
- LinkedIn profile, availability or notice period.
- Dates and hours of the four courses.
"""
(B.OUT / "hedaya-nouman_cv_content_ar-en_v01.md").write_text(head + body + tail, encoding="utf-8")
print("content written")
