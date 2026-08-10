# Course calendar data — `docs/calendar/ics/`

This folder holds one `.ics` file per course. The multi-course calendar at the
site root (`#calendar` section) fetches every course listed in the `COURSES`
config in `docs/calendar/calendar.js`, so **adding a course = adding one
config object + one `.ics` file.**

## Status

**Active.** `cs401.ics` carries the real 2026-06-22 – 2026-09-12 term, anchored
to the actual teaching pace (Week 8 starts 2026-08-11 — confirmed by the
instructor, working backward/forward from there at 5 class days/week:
Mon/Tue/Thu/Fri/Sat, per the 4th-sem timetable's Mon/Tue/Fri/Sat lecture slots
plus the Thursday lab). Week 8 is short one day (Monday 2026-08-10 is a
holiday, so it starts Tuesday instead).

Each week's `Lecture N` event is repeated on all of that week's real class
days (5, except Week 8's 4) rather than posted once — so the month grid shows
one pill per actual class session. `Assignment N Due` covers the 7 published
assignments; three `Class Test N (Unit ...)` events are included.
`semesterStart`/`semesterEnd` are set on the `CS401` object in
`docs/calendar/calendar.js`.

Assignment due dates and Class Test dates were inferred (end of each teaching
week / after each ~4-lecture unit) — adjust the `DTSTART`/`DTEND` lines below
directly if the real dates differ. `docs/calendar/ics/cs401.ics` is generated
from a small script (not committed) rather than hand-edited line by line —
regenerate the same way if the pace or roster of lecture titles changes again.

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
