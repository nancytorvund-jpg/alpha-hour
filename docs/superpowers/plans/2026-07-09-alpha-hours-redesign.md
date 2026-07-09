# Alpha Hours Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite all 13 files in `/Users/nancytorvund/alpha-hour` to the redesigned program: one 2-hour block per weekday evening, two 4-hour Saturday blocks, $4,500/$3,500 session pricing, renamed "Alpha Hours".

**Architecture:** This is a documentation repo with one story told in four formats (markdown, HTML, OPML/workflowy outlines, docx). Each task rewrites one format-group completely, verifies with grep and arithmetic, and commits. The docx files are regenerated from the finished markdown. A final task verifies cross-file consistency, which this repo has drifted on before.

**Tech Stack:** Plain files. Git. pandoc or macOS `textutil` for docx generation.

**Spec:** `docs/superpowers/specs/2026-07-09-alpha-hours-redesign-design.md` (read it first; it is the source of truth).

## Global Constraints

- Program name: **Alpha Hours** (plural) everywhere. Possessive is **Alpha Hours'**. Title: **Head of Alpha Hours**. Repo slug stays `alpha-hour`.
- Writing rules: **no em dashes anywhere**, no AI-marketing vocabulary, no numeric self-ratings. Match the existing documents' voice.
- Commit after every task with author `Nancy Wisniewski Torvund <nancy.torvund@alpha.school>` and trailer `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`. Do not push until the final task.
- Enrollment counts, campus roster, room capacities, feeder math (8-12%, $160k-325k, $40-60M pilot, $225-340M national), central team costs ($0.78M pilot / $3.5M national), session calendar (5 x 7 weeks, ~35 weeks), and staffing ratios (1:10 plus lead, two-adult minimum) are all **unchanged**.

### Canonical number replacements (old → new)

| Item | Old | New |
|---|---|---|
| Session price premium / standard | $3,200 / $2,500 | **$4,500 / $3,500** |
| Full year premium / standard | $16,000 / $12,500 | **$22,500 / $17,500** |
| Hours per session / per week | 14 / 2 | **28 / 4** |
| Per-hour figure | $228, "inside" elite 1:1 range | **$161, "just under"** elite 1:1 range |
| Session vs priciest mainstream competitor (~$875/7wk) | "more than three times" | **"four to five times"** |
| Year vs full Alpha tuition | "25 to 30 percent" | **"roughly a third (30 to 40 percent)"** |
| Pilot revenue / site profit / margin | $27.52M / $23.48M / ~85% | **$38.70M / $33.53M / ~87%** |
| Pilot net after central | $22.7M | **$32.7M** |
| Pilot at 50% fill (rev / site profit) | $13.8M / $11.7M | **$19.4M / $15.8M** |
| Site rows NYC and Boston B (rev / profit / margin) | $6.40M / $5.46M and $5.48M / 85-86% | **$9.00M / $7.81M / 87%** (both) |
| Greenwich | $5.12M / $4.37M / 85% | **$7.20M / $6.23M / 87%** |
| Palm Beach | $3.84M / $3.29M / 86% | **$5.40M / $4.70M / 87%** |
| Miami Beach | $3.20M / $2.73M / 85% | **$4.50M / $3.90M / 87%** |
| Boston A | $2.56M / $2.16M / 84% | **$3.60M / $3.07M / 85%** |
| National revenue | $174.7M (~$175M) | **$245.7M (~$246M)** |
| National site profit / net | ~$149M / ~$146M | **~$213M / ~$210M** |
| "profit engine" phrase | "$140 million-plus" | **"$200 million-plus"** |
| Austin, Chicago rows | $19.20M each | **$27.00M each** |
| Miami row | $9.60M | **$13.50M** |
| National NYC / Boston rows | $6.40M | **$9.00M** |
| National Greenwich / Palm Beach / Miami Beach / Boston Suburbs rows | $5.12M / $3.84M / $3.20M / $2.56M | **$7.20M / $5.40M / $4.50M / $3.60M** |
| Every 50-seat campus row (31 campuses) | $3.20M | **$4.50M** |
| One-pager "35 more campuses" row | $113.9M | **$160.2M** |
| Ramp revenue Y1/Y2/Y3 | ~$14M / ~$50M / ~$100M | **~$19M / ~$68M / ~$135M** |
| Ramp site profit Y1/Y2/Y3 | ~$12M / ~$41M / ~$82M | **~$16M / ~$57M / ~$113M** |
| Ramp net Y1/Y2/Y3 | ~$11M / ~$40M / ~$80M | **~$15M / ~$55M / ~$110M** |
| "reaches roughly $100M by Year 3, toward ~$175M" | | **"$135M ... toward ~$246M"** |
| TAM | ~$70B (4.4M students at $16,000) | **~$99B (4.4M students at $22,500)** |
| SAM | ~$28B | **~$39B** |
| SOM today | ~$175M | **~$246M** |
| "priced at $16,000 a year" (Section 3 lead) | | **"priced at $22,500 a year"** |
| Guide staff week | ~11 hours (2.75h x 4 evenings) | **~20 hours (2.5h x 4 evenings + ~10h Saturday)** |
| Facility fee per site | ~$35,000 | **~$45,000** |
| Marginal facility cost | "$150 to $250 per evening" | **"$150 to $250 per weekday evening, about $400 per Saturday"** |
| Insight 3 job length | "An 11-hour evening-only job" | **"A 20-hour evenings-and-Saturday job"** |

SOM ratios stay "about 0.6% of SAM" and "roughly 0.25% of TAM". Feeder figures unchanged.

### Canonical copy blocks (use verbatim, adapt only markup)

**Schedule, weekday (replaces the old 4-row block table in every file):**

| | Time |
|---|---|
| Setup | 4:45 to 5:00 pm (guides prepare, devices ready) |
| Block | 5:00 to 7:00 pm |
| Dismissal and reset | 7:00 to 7:15 pm |

**Schedule, Saturday (new table, added wherever the weekday table appears):**

| | Time |
|---|---|
| Setup | 8:45 to 9:00 am |
| AM block | 9:00 am to 1:00 pm |
| Transition | 1:00 to 2:00 pm (staggered pickup and drop-off; no lunch served) |
| PM block | 2:00 to 6:00 pm |
| Reset | 6:00 to 6:15 pm |

**Cohort sentence (replaces every "four cohorts a week: Monday/Wednesday early..." sentence):**
"Every campus runs four cohorts a week: Monday/Wednesday, Tuesday/Thursday, Saturday morning, and Saturday afternoon. The same room and the same guide team serve all four, and every cohort gets the same four weekly hours."

**Capacity formula (replaces "room capacity x 2 time blocks x 2 weekly tracks"):**
"Enrolled students per campus is four times the room capacity: two weekday tracks plus two Saturday blocks. A 100-seat room fills to 400 enrolled students."

**Program model paragraph (replaces the "distills that into a single focused hour" paragraph in the business plan, and its shorter variants elsewhere):**
"A normal Alpha day gives students about two hours of core academics on Timeback. Alpha Hours delivers that same two-hour academic day, after school. A family picks a two-night track, Monday/Wednesday or Tuesday/Thursday at 5:00 to 7:00 pm, or a single Saturday block of four hours, morning or afternoon. Either way the child gets four hours a week on the platform, the full Alpha academic dose, roughly half on Math and half on Reading/Writing, adjusting to wherever they need the time. The software delivers the instruction and adapts to each child. The guide manages focus, effort, and motivation. That is the whole model: the complete Alpha academic day, mastery-based, four hours a week."

**Truth 1 (replaces the whole truth, title and body, in all four BrainLift files):**
Title: "Truth 1: Your child gets Alpha's entire academic day here, and it beats the six hours they sat through this morning."
Body: "Alpha's own data claims about 2x learning in roughly two hours a day. Alpha Hours does not sample that, it delivers the whole dose: the same two hours Alpha's own students run, either as two focused evenings or one Saturday sitting. Every family who pays for Alpha Hours is running an experiment that indicts the school they already write checks to. We do not really compete with Kumon. We compete with the six hours their child sat through earlier that day, and we win."

**Truth 7 body sentence:** "There is no homework, because the hours are the work." (rest of the truth unchanged)

**Insight 1 (title and first sentence change, in all four BrainLift files):**
Title: "Insight 1: The unit of the business is the campus operating day, not the student."
Body: "Facility, coordinator, and security costs are per-day and fixed. Software and guide costs are per-student and variable. Profit comes from loading as many students as safely possible onto each fixed campus day, which is why filling all four cohorts matters more than squeezing price."

**Insight 3 body (all four BrainLift files):**
"A 20-hour evenings-and-Saturday job has chronic turnover. A daytime-plus-evening role at $50,000 to $85,000 is a real career, attracts stronger people, and shares the guide's cost with the campus. The staffing model is the hidden make-or-break of a nationwide rollout."

**Licensing sentence (replaces "The one-hour, single-purpose, curriculum-driven design strengthens the instruction argument in every state."):**
"Every block is a curriculum-driven instructional period; the Saturday four-hour block is structured as two two-hour instructional periods with a supervised break, and no lunch is served. Flag the Saturday format specifically in each state's written exemption request."

**Pricing per-hour bullet (business plan and one-pager):**
"We sell a place, not hours. A session is four hours a week for seven weeks, about 28 hours. At $4,500 that is roughly $161 an hour, just under elite 1:1 tutors ($200 to $300), who cover one subject; we cover two, supervised, with the data to prove progress. The program is priced against the outcome and against full Alpha tuition, not against a clock. Quote the session and full-year numbers in marketing; the per-hour figure is for objection handling only."

**Guide evening bullet (Section 5 site team table, business plan):**
"Dedicated Alpha Hours guides. Weekday evenings run about 2.5 hours (4:45 to 7:15 with setup and reset), four evenings a week, plus a roughly 10-hour Saturday, about 20 staff-hours a week. Guides can also work Alpha campus afternoon shifts. A blended daytime-plus-evening role is a real full-time job at roughly $50,000 to $85,000 depending on metro, which attracts stronger candidates and cuts turnover."

**README model paragraph (replaces "The model in one paragraph" body):**
"The full Alpha academic day, after school. Both subjects (Math and Reading/Writing), mixed K-8, four hours a week on Timeback. Each family picks a two-night track, Monday/Wednesday or Tuesday/Thursday from 5:00 to 7:00 pm, or a single four-hour Saturday block, morning or afternoon. Four cohorts share every room, so a campus enrolls four times its seat count. Families enroll one seven-week session at a time; there are five sessions a year. Priced above every competitor at $4,500 per session in premium markets, about a third of full Alpha tuition."

---

### Task 1: Rewrite BUSINESS-PLAN.md

**Files:**
- Modify: `BUSINESS-PLAN.md` (all 11 sections + 7A)

**Interfaces:**
- Produces: the finished markdown that Task 9 converts to `Alpha-Hours-Business-Plan.docx`. Later HTML tasks must match its numbers exactly.

- [ ] **Step 1: Apply every row of the canonical number table and every canonical copy block.** Sections needing prose surgery beyond find-replace: Section 1 (name, "one hour" phrasing), Section 2 (program model paragraph, both schedule tables, cohort sentence, capacity formula), Section 4 (price table, all three bullets including the per-hour block), Section 5 (guide bullet, staff-week), Section 6 (cost bullets: guide hours ~20/wk, facility $45k; full pilot table; ramp paragraph; feeder bullets keep 1,720 and $40-60M), Section 7 (ramp table), Section 7A (all 40 rows, totals, network table), Section 8 (facility costs, licensing sentence), Section 9 (unchanged except name), Section 11 (name only). The title/prepared-by header keeps the date July 9, 2026.
- [ ] **Step 2: Verify.**
Run: `grep -nE '\$3,200|\$2,500|\$16,000|\$12,500|\$27\.5|\$174\.7|\$175M|\$146M|6:15 to 7:15|single focused hour|one focused hour|14 hours|\$228|Alpha Hour[^s]' BUSINESS-PLAN.md`
Expected: no output (note: `Alpha Hour[^s]` also catches possessive errors).
Run the arithmetic check: pilot rows sum to 1,720 and $38.70M; 7A rows sum to 10,920 and $245.7M (sum the table cells with awk as done before).
- [ ] **Step 3: Commit** `git add BUSINESS-PLAN.md && git commit -m "Rewrite business plan for the Alpha Hours redesign"` (with the standard author flags and trailer).

### Task 2: Rewrite EXECUTIVE-ONE-PAGER.md

**Files:**
- Modify: `EXECUTIVE-ONE-PAGER.md`

**Interfaces:**
- Consumes: canonical blocks; numbers must match Task 1 exactly.
- Produces: source for `Alpha-Hours-One-Pager.docx` (Task 9).

- [ ] **Step 1: Apply the same replacements in one-pager form.** Specifics: title and every name plural; "How it runs" bullets get the two-night-track-or-Saturday framing and "four cohorts: Mon/Wed, Tue/Thu, Saturday AM, Saturday PM"; pricing table $4,500/$3,500 and $22,500/$17,500; pilot table rows and totals from the canonical table; "even at 50% fill nets about $15.8M"; ramp table; national tiles ~$246M / ~$210M / $225-340M; market table TAM ~$99B, SAM ~$39B, today ~$246M/yr (0.6% of SAM); the ask keeps five markets, six campuses, names her Head of Alpha Hours.
- [ ] **Step 2: Verify.** Same grep as Task 1 against this file, expected no output. Cross-check: `grep -c '38.7\|33.5\|32.7' EXECUTIVE-ONE-PAGER.md` returns at least 3.
- [ ] **Step 3: Commit** `git commit -m "Rewrite executive one-pager for Alpha Hours"`.

### Task 3: Rewrite README.md and BUSINESS-MODEL.opml

**Files:**
- Modify: `README.md`, `BUSINESS-MODEL.opml`

- [ ] **Step 1: README.** Title "# Alpha Hours"; description sentence keeps the three jobs; swap in the canonical README model paragraph; headline numbers: pilot 1,720 / ~$38.7M / ~$32.7M net / $40-60M feeder; national ~$246M / ~$210M / $225-340M / "about 0.6% of a ~$39B serviceable market"; contents table renames the docx rows to `Alpha-Hours-One-Pager.docx` / `Alpha-Hours-Business-Plan.docx`; audit disclaimer unchanged.
- [ ] **Step 2: BUSINESS-MODEL.opml.** XML-escape any `&`. Update nodes: program (two-hour sittings, four hours a week, Saturday option), schedule (both canonical tables as outline nodes, cohort sentence), capacity (formula wording, x4 via two tracks + two Saturday blocks), enrollment (unchanged), real estate ($150-250 weekday / ~$400 Saturday, facility largely intracompany), team (guide ~20 staff-hours, Head of Alpha Hours), compliance (licensing sentence), pricing node ($4,500/$3,500, $22,500/$17,500, four to five times competitor, roughly a third of Alpha).
- [ ] **Step 3: Verify.** `grep -nE '\$3,200|\$2,500|Alpha Hour[^s]|6:15' README.md BUSINESS-MODEL.opml` expected empty; `xmllint --noout BUSINESS-MODEL.opml` (or `python3 -c "import xml.dom.minidom,sys;xml.dom.minidom.parse('BUSINESS-MODEL.opml')"`) exits 0.
- [ ] **Step 4: Commit** `git commit -m "Update README and business-model outline for Alpha Hours"`.

### Task 4: Rewrite the three BrainLift outline/markdown files

**Files:**
- Modify: `BRAINLIFT.md`, `BRAINLIFT-workflowy.txt`, `BRAINLIFT.opml`

- [ ] **Step 1: Apply to all three, keeping each file's format.** Changes: name plural throughout; Purpose primary-purpose paragraph becomes: "Design and run Alpha Hours: a premium after-school program that delivers the full Alpha academic day on Timeback to K-8 students who do not attend Alpha. Families attend four hours a week: a two-night track (Monday/Wednesday or Tuesday/Thursday, 5:00 to 7:00 pm) or a single four-hour Saturday block, all inside existing Alpha campuses. It covers both subjects (Math and Reading/Writing) every sitting, and enrolls families one seven-week session at a time, five sessions a year."; Truth 1 canonical block; Truth 7 sentence; Insight 1 canonical block; Insight 3 canonical block; Insight 2 keeps its logic but "$3,200 a session" becomes "$4,500 a session"; Insight 4 gets the licensing sentence appended in place of its final clause about exemption; the workflowy/opml Business Model and Financials sections get the same schedule/capacity/pricing/financial updates as Tasks 1-3 (pilot rows, $38.70M/$33.53M/$32.7M, ramp ~$19M/~$68M/~$135M rev and ~$15M/~$55M/~$110M net, national $245.7M/~$210M, TAM ~$99B, SAM ~$39B, facility $45k, guide ~20 hours).
- [ ] **Step 2: Verify.** `grep -nE '\$3,200|\$2,500|\$16,000|\$12,500|Alpha Hour[^s]|one hour|one focused|6:15|11-hour|campus-evening' BRAINLIFT.md BRAINLIFT-workflowy.txt BRAINLIFT.opml` expected empty ("in one hour" phrasings must all be gone). XML-validate the opml.
- [ ] **Step 3: Commit** `git commit -m "Rewrite BrainLift for the Alpha Hours redesign"`.

### Task 5: Rewrite business-plan.html

**Files:**
- Modify: `business-plan.html`

- [ ] **Step 1:** Mirror Task 1 exactly in the HTML: `<title>Alpha Hours — Business Plan</title>`, header, every section, both schedule tables (keep the existing `.tscroll` table markup), pilot and 7A tables, network totals, licensing paragraph. Numbers must be byte-identical to BUSINESS-PLAN.md's.
- [ ] **Step 2: Verify.** Task 1's grep against this file, expected empty. Arithmetic sums on the two tables as before (awk over the `<td class="r">` cells).
- [ ] **Step 3: Commit** `git commit -m "Rewrite business plan HTML for Alpha Hours"`.

### Task 6: Rewrite one-pager.html

**Files:**
- Modify: `one-pager.html`

- [ ] **Step 1:** Mirror Task 2 in the HTML. Specifics beyond find-replace: `<title>Alpha Hours — Executive One-Pager</title>`; thesis line becomes "The full Alpha academic day, run after school and on Saturdays, in the buildings Alpha already pays for."; "How it runs" reason cards get the new track/Saturday copy; spotlight tiles $38.7M / ~87% / $40-60M; pilot table rows; caption "$15.8M at 50% fill" and "nets roughly $32.7M at capacity"; ramp table; national tiles ~$246M / ~$210M / $225-340M; largest-campuses table ($27.00M, $27.00M, $13.50M, $9.00M, $9.00M, "35 more campuses ... $160.2M", total $245.7M); market caption 0.6% of ~$39B inside ~$99B; timeline and ask sections name-only changes.
- [ ] **Step 2: Verify.** Same grep, expected empty; largest-campuses cells sum to 10,920 and $245.7M.
- [ ] **Step 3: Commit** `git commit -m "Rewrite one-pager HTML for Alpha Hours"`.

### Task 7: Rewrite brainlift.html

**Files:**
- Modify: `brainlift.html`

- [ ] **Step 1:** Mirror Task 4 in the HTML: title, header, Purpose paragraph, Truth 1 `.spov` block, Truth 7 sentence, Insight 1 and 3 paragraphs, Insight 2 price, licensing insight, knowledge-tree entries unchanged except any "Alpha Hour" name hits.
- [ ] **Step 2: Verify.** Task 4's grep against this file, expected empty.
- [ ] **Step 3: Commit** `git commit -m "Rewrite BrainLift HTML for Alpha Hours"`.

### Task 8: Rewrite national-buildout.html

**Files:**
- Modify: `national-buildout.html`

- [ ] **Step 1:** Title/eyebrow to Alpha Hours; funnel: TAM ~$99B, SAM ~$39B, Today ~$246M (keep bar widths; the som-note already says bars are not to scale); som-note text: "at $22,500 a year", "about 0.6% of the serviceable market"; both roster tables: flagship rows per the canonical table ($27.00M x2, $13.50M, $9.00M x2, $7.20M, $5.40M, $4.50M, $3.60M) and all 31 standard rows 200 / $4.50M; totals strip: 40 campuses, 10,920, $245.7M, ~$210M, $225-340M; footnote: "(enrolled is four cohorts, room capacity x 4, from two weekday tracks and two Saturday blocks) ... Premium pricing of $4,500 per session ($22,500 per year) at every campus."
- [ ] **Step 2: Verify.** `grep -nE '\$3,200|\$16,000|174\.7|\$146M|\$70B|\$28B|Alpha Hour[^s]' national-buildout.html` expected empty; roster cells sum to 10,920 and $245.7M.
- [ ] **Step 3: Commit** `git commit -m "Rewrite national build-out appendix for Alpha Hours"`.

### Task 9: Regenerate and rename the docx files

**Files:**
- Delete: `Alpha-Hour-One-Pager.docx`, `Alpha-Hour-Business-Plan.docx`
- Create: `Alpha-Hours-One-Pager.docx`, `Alpha-Hours-Business-Plan.docx`

- [ ] **Step 1: Pick a converter.** Run `which pandoc`. If found: `pandoc EXECUTIVE-ONE-PAGER.md -o Alpha-Hours-One-Pager.docx` and `pandoc BUSINESS-PLAN.md -o Alpha-Hours-Business-Plan.docx`. If not found: convert the HTML with textutil: `textutil -convert docx business-plan.html -output Alpha-Hours-Business-Plan.docx` (and same for the one-pager); if textutil garbles the CSS-heavy files, generate from markdown rendered to simple HTML first (`python3 -m pip install markdown` is NOT needed; use `pandoc` via `brew install pandoc` only with Nancy's OK, otherwise textutil on a plain-HTML render).
- [ ] **Step 2: Verify.** `unzip -p Alpha-Hours-Business-Plan.docx word/document.xml | grep -o '4,500\|22,500\|38.70M\|245.7M' | sort -u` shows all four values; same-style check on the one-pager. Both old files gone: `ls Alpha-Hour-*.docx` errors.
- [ ] **Step 3: Commit** `git rm Alpha-Hour-One-Pager.docx Alpha-Hour-Business-Plan.docx && git add Alpha-Hours-*.docx && git commit -m "Regenerate Word exports under the Alpha Hours name"`.

### Task 10: Repo-wide verification and push

**Files:**
- Read-only sweep of all 13 files.

- [ ] **Step 1: Full-repo grep.**
Run: `grep -rnE '\$3,200|\$2,500|\$16,000|\$12,500|\$27\.5|174\.7|\$175M|\$146M|\$70B|\$28B|6:15 to 7:15|one focused hour|single focused hour|11-hour|\$228|Alpha Hour([^s]|$)' --include='*.md' --include='*.html' --include='*.txt' --include='*.opml' .`
Expected: matches only inside `docs/superpowers/` (the spec and this plan legitimately contain old values). Zero matches in the 11 text/markup product files.
- [ ] **Step 2: Cross-file number agreement.** For each of `38.70M|38.7M`, `33.5M`, `32.7M`, `245.7M|246M`, `210M`, `99B`, `39B`, `4,500`, `22,500`: confirm present in every file that states that figure (business plan, one-pager, README, national build-out, BrainLift financials sections as applicable).
- [ ] **Step 3: Push.** `git push origin main` and confirm `git status -sb` shows `## main...origin/main` clean.

## Self-review notes

- Spec coverage: schedule (Tasks 1-8), pricing (all), staffing (1, 3, 4), licensing (1, 4, 5, 7), rename incl. docx (all, 9), verification (10). Repo rename explicitly out of scope.
- The grep patterns use `Alpha Hour([^s]|$)` so "Alpha Hours" passes while singular names, bad possessives, and end-of-line occurrences all fail. Per-task greps may use the shorter `Alpha Hour[^s]`; Task 10's repo-wide sweep uses the full pattern.
- Numbers in later tasks are copied from the canonical table, not recomputed, so cross-task drift cannot occur if implementers use the table.
