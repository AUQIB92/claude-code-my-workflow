# Course calendar data — `docs/calendar/ics/`

This folder holds one `.ics` file per course. The multi-course calendar at the
site root (`#calendar` section) fetches every course listed in the `COURSES`
config in `docs/calendar/calendar.js`, so **adding a course = adding one
config object + one `.ics` file.**

## Status

**Active.** `cs401.ics` carries the real 2026-05-05 – 2026-07-28 term (per the
4th-sem timetable, `docs/Timetable/4th Sem Time Table (2024).pdf`, w.e.f.
05-05-2026): one `Lecture N` event per week (Mon/Tue/Fri/Sat 10:15–11:00 per
the timetable; the flagship weekly event is placed on the week's first class
day), `Assignment N Due` for the 7 published assignments, and three
`Class Test N (Unit ...)` events. `semesterStart`/`semesterEnd` are set on the
`CS401` object in `docs/calendar/calendar.js`.

Assignment due dates and Class Test dates were inferred (end of each teaching
week / after each ~4-lecture unit) — adjust the `DTSTART`/`DTEND` lines below
directly if the real dates differ.

## Expected event formats (CS401)

The classifier in `docs/calendar/calendar.js` (`course.classify`) maps ICS
`SUMMARY` lines to event kinds:

| Kind       | SUMMARY pattern                | Example                          |
|------------|--------------------------------|----------------------------------|
| Lecture    | `Lecture <n> · <title>`        | `Lecture 02 · Number Systems & Arithmetic` |
| Assignment | `Assignment <n> Due`           | `Assignment 1 Due`               |
| Test       | `Class Test <n> (…)` / exam    | `Class Test 1 (Unit I)`          |

## Minimal `.ics` template

```ics
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AUQIB92//Course Calendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:cs401-2026-02-lecture@auqib92.github.io
DTSTART;VALUE=DATE:20260914
DTEND;VALUE=DATE:20260914
SUMMARY:Lecture 02 · Number Systems & Arithmetic
END:VEVENT
BEGIN:VEVENT
UID:cs401-2026-01-assignment@auqib92.github.io
DTSTART;VALUE=DATE:20260918
DTEND;VALUE=DATE:20260918
SUMMARY:Assignment 1 Due
END:VEVENT
BEGIN:VEVENT
UID:cs401-2026-ct1@auqib92.github.io
DTSTART;VALUE=DATE:20261005
DTEND;VALUE=DATE:20261005
SUMMARY:Class Test 1 (Unit I)
END:VEVENT
END:VCALENDAR
```

Timed events use `DTSTART;TZID=Asia/Kolkata:20260914T100000` — the parser
resolves TZID offsets via `Intl` (DST-aware), and all-day events use
`VALUE=DATE`.
