/* ============================================================
   Multi-course teaching calendar — docs/calendar/calendar.js
   ------------------------------------------------------------
   Self-contained, no build step. A course-aware generalization
   of the appliedcryptography.page calendar (see reference/).

   HOW TO ACTIVATE A COURSE:
   1. Drop an .ics file into docs/calendar/ics/<code>.ics
   2. In the COURSES config below set icsUrl, semesterStart,
      semesterEnd, defaultTz and fill the topics slug map.
   Until then the section renders a "term dates pending" empty
   state. Adding a course = one config object + one .ics.
   ============================================================ */

(function () {
	"use strict";

	/* ──────────────  Icons (inline SVG, currentColor)  ────────────── */

	const svg = (paths, vb) =>
		`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb || "0 0 24 24"}" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths}</svg>`;

	const ICONS = {
		calendar: svg('<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M8 2v4M16 2v4M3 9h18"/>'),
		list: svg('<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>'),
		presentation: svg('<rect x="3" y="3" width="18" height="12" rx="2"/><path d="M12 15v4M8 22l4-3 4 3M8 9l2.5-2.5M16 9l-2.5-2.5"/>'),
		clipboard: svg('<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4a2 2 0 0 1 6 0M9 13l2 2 4-4"/>'),
		"file-check": svg('<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 15l2 2 4-4"/>'),
		download: svg('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>'),
		rss: svg('<path d="M4 11a9 9 0 0 1 9 9M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1.5" fill="currentColor" stroke="none"/>'),
		google: svg('<path d="M12 5.5c1.8 0 3.4.6 4.7 1.8l2.4-2.4C17.3 3.2 14.8 2 12 2 7.6 2 3.9 4.8 2.2 8.8l2.9 2.3C6.1 8.1 8.8 5.5 12 5.5z"/><path d="M21.5 12.2c0-.8-.1-1.4-.2-2H12v4h5.4c-.2 1.2-.9 2.2-1.9 2.9l2.9 2.2c1.7-1.6 3.1-3.9 3.1-7.1z" fill="currentColor" stroke="none"/><path d="M5.1 14.1c-.5-.9-.8-2-.8-3.1s.3-2.2.8-3.1L2.2 5.6C1 7.5.3 9.7.3 12s.7 4.5 1.9 6.4l2.9-2.3z" fill="currentColor" stroke="none"/>'),
		quiz: svg('<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 0 1 4.9.8c0 1.6-2.4 2.1-2.4 3.7"/><path d="M12 17h.01"/>'),
		"map-pin": svg('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
		"arrow-up": svg('<path d="M12 19V5M5 12l7-7 7 7"/>'),
		"calendar-x": svg('<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M8 2v4M16 2v4M3 9h18M9 14l6 6M15 14l-6 6"/>'),
		clock: svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
		"book-open": svg('<path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2zM22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z"/>'),
	};

	/* ──────────────  Course registry  ──────────────
	   semesterStart/End: ms since epoch (UTC). null = term dates pending.
	   topics: lecture slug map so events can link to the deployed PDFs.
	   classify(raw): map an ICS VEVENT summary to {kind, chip, title, links}.
	   kinds: the event kinds this course uses.                        */

	const COURSES = [
		{
			code: "CS401",
			short: "CS-401",
			title: "Computer Organization & Architecture",
			icsUrl: "calendar/ics/cs401.ics",
			semesterStart: 1777939200000, // 2026-05-05T00:00:00Z (per 4th-sem timetable, w.e.f. 05-05-2026)
			semesterEnd: 1785283199000, // 2026-07-28T23:59:59Z (12 teaching weeks)
			defaultTz: "Asia/Kolkata", // GCET Kashmir, fixed IST regardless of viewer
			kinds: ["lecture", "assignment", "test"],
			topics: {
				"1": "intro-performance",
				"2": "number-systems-arithmetic",
				"3": "ieee754-floating-point",
				"4": "registers-instructions",
				"5": "addressing-cpu-bus",
				"6": "hardwired-control",
				"7": "microprogrammed-control",
				"8": "io-techniques",
				"9": "cache-memory",
				"10": "virtual-memory-storage",
				"11": "parallel-pipeline-hazards",
				"12": "pipelining-risc-cisc",
			},
			classify(raw) {
				const s = raw.summary || "";
				const pad = (n) => String(n).padStart(2, "0");

				// "Lecture 02 · Number Systems & Arithmetic"
				let m = s.match(/^Lecture\s+(\d{1,2})\s*[·|]\s*(.+)$/);
				if (m) {
					const n = +m[1];
					const slug = this.topics[String(n)];
					const href = slug ? `slides/CS401/${pad(n)}-${slug}.pdf` : null;
					const links = [];
					if (href) links.push({ label: "Slides", icon: "presentation", primary: true, href });
					if (slug) links.push({ label: "Notes", icon: "book-open", href: `notes/CS401/${pad(n)}-${slug}.pdf` });
					if (slug) links.push({ label: "GATE practice", icon: "quiz", href: `gate/CS401/${pad(n)}-${slug}.pdf` });
					return {
						kind: "lecture",
						chip: `L${n}`,
						title: `Week ${n} · ${m[2].trim()}`,
						links,
					};
				}

				// "Assignment 1 Due"
				m = s.match(/^Assignment\s+(\d{1,2})\s*Due$/i);
				if (m) {
					const n = +m[1];
					const slug = this.topics[String(n)];
					const base = slug ? `assignments/CS401/${pad(n)}-${slug}` : null;
					const links = [];
					if (base) links.push({ label: "Problem", icon: "clipboard", primary: true, href: `${base}-assignment.pdf` });
					if (base) links.push({ label: "Solutions", icon: "file-check", href: `${base}-solutions.pdf` });
					return {
						kind: "assignment",
						chip: `A${n}`,
						title: `Assignment ${n}`,
						links,
					};
				}

				// "Class Test 1 (Unit I)" / "Mid-Term" / "Final Exam"
				m = s.match(/^Class Test\s+(\d{1,2})/i);
				if (m) {
					return { kind: "test", chip: `CT${m[1]}`, title: s.trim(), links: [] };
				}
				if (/exam|mid|final|end-semester/i.test(s)) {
					return { kind: "test", chip: /final/i.test(s) ? "Final" : "Mid", title: s.trim(), links: [] };
				}

				console.warn("[calendar] unclassified event:", s);
				return null;
			},
		},
	];

	const VALID_KINDS = ["lecture", "assignment", "test"];

	/* ──────────────  ICS parsing (RFC 5545 subset)  ────────────── */

	const unfoldICS = (text) => {
		const lines = text.replace(/\r\n/g, "\n").split("\n");
		const out = [];
		for (const line of lines) {
			if (line.startsWith(" ") || line.startsWith("\t")) {
				out[out.length - 1] += line.slice(1);
			} else {
				out.push(line);
			}
		}
		return out;
	};

	const tzOffsetMs = (tz, date) => {
		try {
			const dtf = new Intl.DateTimeFormat("en-US", {
				timeZone: tz,
				hour12: false,
				year: "numeric", month: "2-digit", day: "2-digit",
				hour: "2-digit", minute: "2-digit", second: "2-digit",
			});
			const map = {};
			dtf.formatToParts(date).forEach((p) => { if (p.type !== "literal") map[p.type] = p.value; });
			const asUTC = Date.UTC(+map.year, +map.month - 1, +map.day, +map.hour, +map.minute, +map.second);
			return asUTC - date;
		} catch (_) {
			return 0;
		}
	};

	const parseICSDateValue = (raw, params) => {
		const tzid = params.TZID || (raw.endsWith("Z") ? "UTC" : null);
		const allDay = !raw.includes("T");
		const y = +raw.slice(0, 4), mo = +raw.slice(4, 6), d = +raw.slice(6, 8);
		if (allDay) {
			return { allDay: true, tz: null, instant: Date.UTC(y, mo - 1, d), y, m: mo, d };
		}
		const h = +raw.slice(9, 11), mi = +raw.slice(11, 13), s = +raw.slice(13, 15);
		const utc = Date.UTC(y, mo - 1, d, h, mi, s);
		const instant = tzid === "UTC"
			? utc
			: tzid
				? utc - tzOffsetMs(tzid, utc)
				: new Date(y, mo - 1, d, h, mi, s).getTime();
		return { allDay: false, tz: tzid || null, instant, y, m: mo, d };
	};

	const parseICS = (text) => {
		const lines = unfoldICS(text);
		const events = [];
		let current = null;
		for (const line of lines) {
			if (line === "BEGIN:VEVENT") { current = {}; continue; }
			if (line === "END:VEVENT") { if (current) events.push(current); current = null; continue; }
			if (!current) continue;
			const colon = line.indexOf(":");
			if (colon < 0) continue;
			const head = line.slice(0, colon);
			const value = line.slice(colon + 1);
			const [name, ...paramParts] = head.split(";");
			const params = {};
			for (const p of paramParts) {
				const eq = p.indexOf("=");
				if (eq > 0) params[p.slice(0, eq)] = p.slice(eq + 1);
			}
			if (name === "DTSTART" || name === "DTEND") current[name.toLowerCase()] = parseICSDateValue(value, params);
			else if (name === "SUMMARY" || name === "LOCATION" || name === "UID") current[name.toLowerCase()] = value;
		}
		return events;
	};

	/* ──────────────  Formatters  ────────────── */

	const DAY_MS = 24 * 60 * 60 * 1000;

	const fmtIn = (instant, tz, opts) =>
		new Intl.DateTimeFormat("en-US", { ...opts, timeZone: tz === "local" || tz == null ? undefined : tz }).format(instant);

	const fmtDow = (i, tz) => fmtIn(i, tz, { weekday: "short" }).toUpperCase();
	const fmtDom = (i, tz) => fmtIn(i, tz, { day: "numeric" });
	const fmtMon = (i, tz) => fmtIn(i, tz, { month: "short" });
	const fmtDate = (i, tz) => fmtIn(i, tz, { weekday: "long", month: "long", day: "numeric" });
	const fmtMonthYear = (i, tz) => fmtIn(i, tz, { month: "long", year: "numeric" });
	const fmtShortDate = (i, tz) => fmtIn(i, tz, { month: "short", day: "numeric" });

	const fmtTimeRange = (startInstant, endInstant, tz) => {
		const t = (x) => fmtIn(x, tz, { hour: "numeric", minute: "2-digit", hour12: false });
		return `${t(startInstant)}–${t(endInstant)}`;
	};

	const tzShortLabel = (tz) => {
		if (tz === "UTC") return "UTC";
		try {
			const parts = new Intl.DateTimeFormat("en-US", { timeZone: tz, timeZoneName: "short" }).formatToParts(Date.now());
			const p = parts.find((x) => x.type === "timeZoneName");
			return p ? p.value : tz;
		} catch (_) { return tz || "Local"; }
	};

	const localTz = () => Intl.DateTimeFormat().resolvedOptions().timeZone;

	const startOfWeekUTC = (instant) => {
		const d = new Date(instant);
		const dow = (d.getUTCDay() + 6) % 7;
		return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate() - dow);
	};

	const fmtWeekHeader = (instant, tz) => {
		const start = startOfWeekUTC(instant);
		const end = start + 6 * DAY_MS;
		return `${fmtShortDate(start, tz)} — ${fmtShortDate(end, tz)}`;
	};

	const isSameDayUTC = (a, b) => {
		const da = new Date(a), db = new Date(b);
		return da.getUTCFullYear() === db.getUTCFullYear() &&
			da.getUTCMonth() === db.getUTCMonth() &&
			da.getUTCDate() === db.getUTCDate();
	};

	const todayInstant = () => {
		const now = new Date();
		return Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
	};

	const monthKeyToInstant = (key) => {
		const { y, m } = monthKeyToParts(key);
		return Date.UTC(y, m, 1);
	};

	const eventDayKey = (instant, tz) => {
		const fmt = new Intl.DateTimeFormat("en-CA", { timeZone: tz || undefined, year: "numeric", month: "2-digit", day: "2-digit" });
		return fmt.format(instant);
	};

	const eventMonthKey = (instant, tz) => eventDayKey(instant, tz).slice(0, 7);

	const monthKeyToParts = (key) => {
		const [y, m] = key.split("-").map(Number);
		return { y, m: m - 1 };
	};

	const buildMonthCells = (key) => {
		const { y, m } = monthKeyToParts(key);
		const first = Date.UTC(y, m, 1);
		const leading = (new Date(first).getUTCDay() + 6) % 7;
		const gridStart = Date.UTC(y, m, 1 - leading);
		const cells = [];
		for (let i = 0; i < 42; i++) {
			const d = new Date(gridStart + i * DAY_MS);
			cells.push({ instant: gridStart + i * DAY_MS, day: d.getUTCDate(), outside: d.getUTCMonth() !== m });
		}
		return cells;
	};

	/* ──────────────  HTML builder  ────────────── */

	const h = (tag, attrs, ...children) => {
		const attrStr = attrs
			? Object.entries(attrs)
				.filter(([, v]) => v !== null && v !== undefined && v !== false)
				.map(([k, v]) => ` ${k}="${String(v).replace(/"/g, "&quot;")}"`)
				.join("")
			: "";
		const inner = children.filter((c) => c !== null && c !== undefined && c !== false && c !== "").join("");
		return `<${tag}${attrStr}>${inner}</${tag}>`;
	};

	/* ──────────────  State / events  ────────────── */

	const eventMonth = (e, tz) => eventMonthKey(e.start.instant, tz);

	const visibleEvents = (events, state) =>
		events.filter((e) =>
			state.courses.includes(e.course.code) && state.kinds.includes(e.kind)
		);

	const eventsOnDay = (events, dayInstant, tz) => {
		const key = eventDayKey(dayInstant, tz);
		return events.filter((e) => eventDayKey(e.start.instant, tz) === key);
	};

	/* ──────────────  Renderers  ────────────── */

	const ribbon = (events, state) => {
		const today = todayInstant();
		const counts = events.reduce((acc, e) => { acc[e.kind] = (acc[e.kind] || 0) + 1; return acc; }, {});
		const spans = events.reduce((acc, e) => {
			acc.min = Math.min(acc.min, e.start.instant);
			acc.max = Math.max(acc.max, e.start.instant);
			return acc;
		}, { min: Infinity, max: -Infinity });
		const active = Number.isFinite(spans.min) && today >= spans.min && today <= spans.max;
		const pct = active
			? Math.min(100, Math.max(0, ((today - spans.min) / (spans.max - spans.min)) * 100))
			: null;
		const nCourses = new Set(events.map((e) => e.course.code)).size;
		return `
			<span class="cal-ribbon-stat">${ICONS.calendar}<strong>${fmtShortDate(spans.min, state.tz)} – ${fmtShortDate(spans.max, state.tz)}</strong></span>
			<span class="cal-ribbon-stat">${ICONS["book-open"]}${nCourses} course${nCourses === 1 ? "" : "s"}</span>
			<span class="cal-ribbon-stat">${ICONS.presentation}${counts.lecture || 0} lectures</span>
			<span class="cal-ribbon-stat">${ICONS.clipboard}${counts.assignment || 0} assignments</span>
			<span class="cal-ribbon-stat">${ICONS["file-check"]}${counts.test || 0} tests</span>
			${pct !== null ? `
				<div class="cal-ribbon-progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${Math.round(pct)}" aria-label="Term progress">
					<div class="cal-ribbon-progress-fill" style="width: ${pct.toFixed(1)}%"></div>
				</div>
			` : ""}`;
	};

	const caption = (state) => `
		<label class="cal-tz-label">Times shown in
			<select class="cal-tz" data-action="set-tz" aria-label="Timezone">
				<option value="local" ${state.tz === "local" ? "selected" : ""}>Your time (${localTz()})</option>
				<option value="utc" ${state.tz === "UTC" ? "selected" : ""}>UTC</option>
			</select>
		</label>
		<span class="cal-legend">
			<span class="cal-legend-item"><span class="cal-legend-dot" data-kind="lecture"></span>Lecture</span>
			<span class="cal-legend-item"><span class="cal-legend-dot" data-kind="assignment"></span>Assignment</span>
			<span class="cal-legend-item"><span class="cal-legend-dot" data-kind="test"></span>Test</span>
		</span>`;

	const toolbar = (state) => {
		const courseBtns = COURSES.map((c) =>
			`<button class="cal-filter cal-filter-course" data-action="toggle-course" data-course="${c.code}"
			        aria-pressed="${state.courses.includes(c.code)}">
				<span class="cal-course-dot" style="--course:${c.color || "#2c5e2a"}"></span>${c.short}
			</button>`
		).join("");
		const kindBtns = VALID_KINDS.map((k) =>
			`<button class="cal-filter" data-action="toggle-kind" data-kind="${k}"
			        aria-pressed="${state.kinds.includes(k)}">
				<span class="cal-legend-dot" data-kind="${k}" aria-hidden="true"></span>${k.charAt(0).toUpperCase() + k.slice(1)}s
			</button>`
		).join("");
		return `
			<div class="cal-tabs" role="tablist" aria-label="Calendar view">
				<button class="cal-tab" role="tab" data-action="set-view" data-view="month" aria-selected="${state.view === "month"}">
					${ICONS.calendar}Month
				</button>
				<button class="cal-tab" role="tab" data-action="set-view" data-view="agenda" aria-selected="${state.view === "agenda"}">
					${ICONS.list}Agenda
				</button>
			</div>
			<div class="cal-filters" role="group" aria-label="Filter courses">${courseBtns}</div>
			<div class="cal-filters" role="group" aria-label="Filter events">${kindBtns}</div>
			<div class="cal-subscribe">
				${state.courseLinks.map((l) => `
					<a href="${l.href}" ${l.download ? `download="${l.download}"` : ""} ${l.external ? `target="_blank" rel="noopener"` : ""} title="${l.title}">
						${ICONS[l.icon]}<span class="cal-sub-label">${l.label}</span>
					</a>`).join("")}
			</div>`;
	};

	const eventCard = (event, state) => {
		const tz = state.tz === "UTC" ? "UTC" : undefined;
		const start = event.start.instant;
		const isToday = isSameDayUTC(start, todayInstant());
		const isAllDay = event.start.allDay;
		const time = isAllDay
			? "All day"
			: `${fmtTimeRange(start, event.end ? event.end.instant : start, state.tz === "UTC" ? "UTC" : localTz())} ${state.tz === "UTC" ? "UTC" : localTz()}`;
		const kindLabel = { lecture: "Lecture", assignment: "Assignment", test: "Test" }[event.kind];
		const kindIcon = { lecture: "presentation", assignment: "clipboard", test: "file-check" }[event.kind];
		const actions = (event.links || []).map((l) =>
			`<a class="cal-event-btn" ${l.primary ? `data-primary="true" ` : ""}href="${l.href}">${ICONS[l.icon]}${l.label}</a>`
		).join("");
		const sub = event.location
			? `<p class="cal-event-sub">${ICONS["map-pin"]}${event.location}</p>`
			: "";
		return `
			<article class="cal-event" data-kind="${event.kind}" data-today="${isToday}">
				<div class="cal-event-date">
					<span class="cal-event-dow">${fmtDow(start, tz)}</span>
					<span class="cal-event-day">${fmtDom(start, tz)}</span>
					<span class="cal-event-mon">${fmtMon(start, tz)}</span>
				</div>
				<div class="cal-event-body">
					<div class="cal-event-meta">
						<span class="cal-event-kind" data-kind="${event.kind}">${ICONS[kindIcon]}${kindLabel}</span>
						<span class="cal-event-course">${event.course.short}</span>
						<span class="cal-event-time">${time}</span>
						${isToday ? `<span class="cal-event-today">Today</span>` : ""}
					</div>
					<h4 class="cal-event-title">${event.title}</h4>
					${sub}
				</div>
				${actions ? `<div class="cal-event-actions">${actions}</div>` : ""}
			</article>`;
	};

	const dayChipLabel = (event) => event.chip || "";

	const monthGrid = (events, state) => {
		const visible = visibleEvents(events, state);
		const cells = buildMonthCells(state.month);
		const today = todayInstant();
		const headers = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((l) => h("th", { scope: "col" }, l));
		const headerRow = h("tr", null, ...headers);

		const renderCell = (cell) => {
			const dayEvents = cell.outside ? [] : eventsOnDay(visible, cell.instant, state.tz === "UTC" ? "UTC" : undefined);
			const shown = dayEvents.slice(0, 3);
			const overflow = dayEvents.length - shown.length;
			const isToday = isSameDayUTC(cell.instant, today);
			const isSelected = state.day === cell.instant;
			const chips = shown.map((e) =>
				h("span", { class: "cal-day-chip", "data-kind": e.kind }, dayChipLabel(e))
			);
			const more = overflow > 0 ? h("span", { class: "cal-day-more" }, `+${overflow} more`) : "";
			return h("td", {
				role: "gridcell",
				"data-outside": String(cell.outside),
				"data-today": String(isToday),
				"data-selected": String(isSelected),
				"data-action": "select-day",
				"data-instant": cell.instant,
				"aria-selected": String(isSelected),
				"aria-label": `${fmtDate(cell.instant, state.tz === "UTC" ? "UTC" : undefined)}, ${dayEvents.length} event${dayEvents.length === 1 ? "" : "s"}`,
				tabindex: isSelected ? "0" : "-1",
			},
				h("span", { class: "cal-day-num" }, cell.day),
				h("div", { class: "cal-day-chips" }, ...chips, more),
			);
		};

		const rows = [0, 1, 2, 3, 4, 5].map((r) =>
			h("tr", null, ...cells.slice(r * 7, r * 7 + 7).map(renderCell))
		);

		return h("div", { class: "cal-month-grid", role: "grid", "aria-label": state.monthLabel },
			h("div", { class: "cal-month-header" }, monthHeader(state)),
			h("table", { class: "cal-month-table" },
				h("thead", null, headerRow),
				h("tbody", null, ...rows),
			),
		);
	};

	const monthHeader = (state) => {
		const idx = state.monthKeys.indexOf(state.month);
		return h("h3", { class: "cal-month-title" }, state.monthLabel) +
			h("div", { class: "cal-month-nav" },
				h("button", { "data-action": "month-prev", "aria-label": "Previous month", disabled: idx <= 0 ? "" : null }, "‹"),
				h("button", { "data-action": "month-next", "aria-label": "Next month", disabled: idx >= state.monthKeys.length - 1 ? "" : null }, "›"),
			);
	};

	const dayPanel = (events, state) => {
		const visible = visibleEvents(events, state);
		if (!state.day) {
			return h("aside", { class: "cal-day-panel" },
				h("p", { class: "cal-day-panel-empty" }, "Select a day to see its events."));
		}
		const dayEvents = eventsOnDay(visible, state.day, state.tz === "UTC" ? "UTC" : undefined);
		const body = dayEvents.length === 0
			? h("p", { class: "cal-day-panel-empty" }, "No events on this day.")
			: dayEvents.map((e) => eventCard(e, state)).join("");
		return h("aside", { class: "cal-day-panel" },
			h("h3", { class: "cal-day-panel-title" }, fmtDate(state.day, state.tz === "UTC" ? "UTC" : undefined)),
			body);
	};

	const monthView = (events, state) => `
		<div class="cal-month">
			${monthGrid(events, state)}
			${dayPanel(events, state)}
		</div>`;

	const agendaView = (events, state) => {
		const visible = visibleEvents(events, state).filter((e) => eventMonth(e, state.tz === "UTC" ? "UTC" : undefined) === state.month);
		const header = `<div class="cal-agenda-header">${monthHeader(state)}</div>`;
		if (visible.length === 0) {
			return `${header}<div class="cal-empty">${ICONS["calendar-x"]}No events match these filters this month.</div>`;
		}
		const groups = new Map();
		for (const e of visible) {
			const key = startOfWeekUTC(e.start.instant);
			if (!groups.has(key)) groups.set(key, []);
			groups.get(key).push(e);
		}
		const sorted = [...groups.entries()].sort(([a], [b]) => a - b);
		return `${header}
			<ol class="cal-agenda" aria-label="${state.monthLabel} events">
				${sorted.map(([weekStart, weekEvents]) => `
					<li class="cal-week">
						<h3 class="cal-week-header">${fmtWeekHeader(weekStart, state.tz === "UTC" ? "UTC" : undefined)}</h3>
						${weekEvents.map((e) => eventCard(e, state)).join("")}
					</li>
				`).join("")}
			</ol>`;
	};

	const emptyState = () => `
		<div class="cal-empty cal-empty-pending">
			${ICONS["calendar-x"]}
			<h3>Term dates pending</h3>
			<p>The course calendar activates as soon as the semester schedule is set. Lectures, assignments, and tests will appear here in month and agenda views — with one click to subscribe or export.</p>
			<p class="cal-empty-hint">No calendar data has been published yet.</p>
		</div>`;

	/* ──────────────  URL state  ────────────── */

	const serializeState = (state) => {
		const parts = [];
		if (state.view !== "month") parts.push(`view=${state.view}`);
		if (state.month !== state.monthKeys[0]) parts.push(`m=${state.month}`);
		if (state.day) {
			const d = new Date(state.day);
			parts.push(`d=${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}-${String(d.getUTCDate()).padStart(2, "0")}`);
		}
		const allCourses = COURSES.map((c) => c.code);
		if (!allCourses.every((c) => state.courses.includes(c))) parts.push(`courses=${state.courses.join(",")}`);
		if (!VALID_KINDS.every((k) => state.kinds.includes(k))) parts.push(`kinds=${state.kinds.join(",")}`);
		if (state.tz === "UTC") parts.push("tz=utc");
		return parts.length ? `calendar?${parts.join("&")}` : "calendar";
	};

	const deserializeState = (hash, defaults) => {
		const state = { ...defaults, courses: [...defaults.courses], kinds: [...defaults.kinds] };
		if (!hash || !hash.startsWith("#calendar")) return state;
		const qi = hash.indexOf("?");
		if (qi < 0) return state;
		const params = new URLSearchParams(hash.slice(qi + 1));
		if (params.has("view") && (params.get("view") === "agenda" || params.get("view") === "month")) state.view = params.get("view");
		if (params.has("m") && state.monthKeys.includes(params.get("m"))) state.month = params.get("m");
		if (params.has("d")) {
			const m = params.get("d").match(/^(\d{4})-(\d{2})-(\d{2})$/);
			if (m) state.day = Date.UTC(+m[1], +m[2] - 1, +m[3]);
		}
		if (params.has("courses")) {
			const codes = params.get("courses").split(",").filter((c) => COURSES.some((cc) => cc.code === c));
			if (codes.length) state.courses = codes;
		}
		if (params.has("kinds")) {
			const ks = params.get("kinds").split(",").filter((k) => VALID_KINDS.includes(k));
			if (ks.length) state.kinds = ks;
		}
		if (params.get("tz") === "utc") state.tz = "UTC";
		return state;
	};

	/* ──────────────  Init  ────────────── */

	const buildState = (events, hash) => {
		const active = COURSES.filter((c) => c.semesterStart != null && c.semesterEnd != null);
		const starts = active.map((c) => c.semesterStart);
		const ends = active.map((c) => c.semesterEnd);
		const minS = Math.min(...starts);
		const maxE = Math.max(...ends);
		const monthKeys = [];
		const cursor = new Date(minS);
		cursor.setUTCDate(1);
		while (Date.UTC(cursor.getUTCFullYear(), cursor.getUTCMonth(), 1) <= maxE) {
			monthKeys.push(`${cursor.getUTCFullYear()}-${String(cursor.getUTCMonth() + 1).padStart(2, "0")}`);
			cursor.setUTCMonth(cursor.getUTCMonth() + 1);
		}
		const defaults = {
			view: "month",
			courses: COURSES.map((c) => c.code),
			kinds: [...VALID_KINDS],
			month: monthKeys[0],
			monthKeys,
			monthLabel: fmtMonthYear(monthKeyToInstant(monthKeys[0]), undefined),
			day: null,
			tz: "local",
			courseLinks: active.map((c) => ({
				href: c.icsUrl,
				download: `${c.code}.ics`,
				label: c.short,
				icon: "download",
				title: `Download ${c.short} .ics`,
			})),
		};
		const state = deserializeState(hash, defaults);
		const idx = Math.max(0, state.monthKeys.indexOf(state.month));
		if (idx < 0) state.month = state.monthKeys[0];
		state.monthLabel = fmtMonthYear(monthKeyToInstant(state.month), undefined);
		if (state.view === "month" && !state.day) {
			const visible = visibleEvents(events, state);
			if (visible.length) {
				const t = todayInstant();
				const todayHas = visible.some((e) => isSameDayUTC(e.start.instant, t));
				state.day = todayHas ? t : visible[0].start.instant;
				const d = new Date(state.day);
				state.month = `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}`;
				state.monthLabel = fmtMonthYear(monthKeyToInstant(state.month), undefined);
			}
		}
		return state;
	};

	window.calendarInit = async () => {
		const section = document.getElementById("calendar");
		if (!section) return;
		const host = section.querySelector("[data-cal-view]");

		const active = COURSES.filter((c) => c.semesterStart != null && c.semesterEnd != null);
		if (active.length === 0) {
			host.innerHTML = emptyState();
			const ribbonHost = section.querySelector("[data-cal-ribbon]");
			if (ribbonHost) ribbonHost.hidden = true;
			return;
		}

		try {
			const allEvents = [];
			for (const course of active) {
				const res = await fetch(course.icsUrl, { cache: "no-cache" });
				if (!res.ok) throw new Error(`HTTP ${res.status} (${course.icsUrl})`);
				const text = await res.text();
				const parsed = parseICS(text)
					.map((raw) => {
						const cls = course.classify.call(course, raw);
						if (!cls) return null;
						return { ...cls, course, start: raw.dtstart, end: raw.dtend, location: raw.location || null, raw };
					})
					.filter(Boolean)
					.sort((a, b) => a.start.instant - b.start.instant);
				allEvents.push(...parsed);
			}
			allEvents.sort((a, b) => a.start.instant - b.start.instant);

			const state = buildState(allEvents, window.location.hash);

			const ribbonHost = section.querySelector("[data-cal-ribbon]");
			const toolbarHost = section.querySelector("[data-cal-toolbar]");
			const captionHost = section.querySelector("[data-cal-caption]");

			const rerender = () => {
				state.monthLabel = fmtMonthYear(monthKeyToInstant(state.month), undefined);
				state.courseLinks = active.map((c) => ({
					href: c.icsUrl,
					download: `${c.code}.ics`,
					label: c.short,
					icon: "download",
					title: `Download ${c.short} .ics`,
				}));
				toolbarHost.innerHTML = toolbar(state);
				host.innerHTML = state.view === "agenda" ? agendaView(allEvents, state) : monthView(allEvents, state);
				captionHost.innerHTML = caption(state);
				const next = `#${serializeState(state)}`;
				if (window.location.hash !== next) history.replaceState(null, "", next);
			};

			ribbonHost.innerHTML = ribbon(allEvents, state);
			ribbonHost.hidden = false;
			rerender();

			section.addEventListener("click", (e) => {
				const target = e.target.closest("[data-action]");
				if (!target) return;
				const action = target.dataset.action;
				if (action === "toggle-course") {
					const code = target.dataset.course;
					state.courses = state.courses.includes(code)
						? state.courses.filter((c) => c !== code)
						: [...state.courses, code];
					rerender();
				} else if (action === "toggle-kind") {
					const kind = target.dataset.kind;
					state.kinds = state.kinds.includes(kind)
						? state.kinds.filter((k) => k !== kind)
						: [...state.kinds, kind];
					rerender();
				} else if (action === "set-view") {
					state.view = target.dataset.view;
					if (state.view === "month") {
						const visible = visibleEvents(allEvents, state);
						const t = todayInstant();
						const todayHas = visible.some((e) => isSameDayUTC(e.start.instant, t));
						state.day = todayHas ? t : (visible[0] ? visible[0].start.instant : null);
						if (state.day) {
							const d = new Date(state.day);
							state.month = `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, "0")}`;
						}
					}
					rerender();
				} else if (action === "month-prev" || action === "month-next") {
					const i = state.monthKeys.indexOf(state.month);
					const ni = action === "month-prev" ? i - 1 : i + 1;
					if (ni >= 0 && ni < state.monthKeys.length) state.month = state.monthKeys[ni];
					rerender();
				} else if (action === "select-day") {
					if (target.dataset.outside === "true") return;
					state.day = Number(target.dataset.instant);
					rerender();
				}
			});

			section.addEventListener("change", (e) => {
				const target = e.target.closest("[data-action='set-tz']");
				if (!target) return;
				state.tz = target.value === "utc" ? "UTC" : "local";
				rerender();
			});

			window.addEventListener("hashchange", () => {
				const next = deserializeState(window.location.hash, {
					...state,
					courses: [...state.courses],
					kinds: [...state.kinds],
				});
				Object.assign(state, next, { courses: [...next.courses], kinds: [...next.kinds] });
				rerender();
			});
		} catch (err) {
			console.error("[calendar] failed", err);
			host.innerHTML = `<div class="cal-error">Couldn't load the calendar. The schedule may not be published yet.</div>`;
		}
	};
})();
