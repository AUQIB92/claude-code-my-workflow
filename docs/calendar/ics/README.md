# Course calendar data — `docs/calendar/ics/`

This folder holds one `.ics` file per course. The multi-course calendar at the
site root (`#calendar` section) fetches every course listed in the `COURSES`
config in `docs/calendar/calendar.js`, so **adding a course = adding one
config object + one `.ics` file.**

## Status

Term dates are **not set yet**, so this folder only contains this README. The
`#calendar` section currently renders an honest "Term dates pending" empty
state. To activate CS401:

1. Create `docs/calendar/ics/cs401.ics` following the format below.
2. In `docs/calendar/calendar.js` set `semesterStart` / `semesterEnd` (ms since
   epoch UTC) on the `CS401` course object (and `defaultTz` if you want a fixed
   timezone instead of browser-local).

No other code changes are needed — the section, filters, month/agenda views,
and subscribe/download buttons light up automatically.

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
