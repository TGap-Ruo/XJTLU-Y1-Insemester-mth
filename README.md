# XJTLU Year 1 question banks — MTH028 + MTH026

Two courses share one site. The **default page is MTH028 (Linear Algebra I)**;
the top bar of each course links to the other one, so you can switch at any
time without losing your place.

**Live:** <http://183.66.27.19:58621/> (server listens on port 8088)

**Maintainer docs:** [`TECH.md`](TECH.md) — runtime flow, every API endpoint, the
data model, the build pipeline, deployment steps and the list of traps. Read that
first before changing anything.

| Course | Entry | Bank | Topics | Glossary |
|---|---|---|---|---|
| **MTH028 · Linear Algebra I** | `/` → `index.html` | 285 templates / 675 records (420 choice · 195 fill · 60 cloze) | 17 sections × 26 sub-topics | 33 groups / 212 terms |
| **MTH026 · Calculus I** | `/mth026.html` | 674 items (351 + 323) | 54 | 9 groups / 80 terms |

Progress is **isolated per course**: MTH028 uses the `progress28` table and the
`api/progress28` endpoint with localStorage key `mth028.en.v1`, while MTH026
keeps its original `progress` table, `api/progress` and `mth026.en.v1`. Both
share the same user accounts and admin console; neither course's answers,
favourites or mistake book can leak into the other.

### MTH028 question bank

- **One unified `items` array.** Every question lives in `bank.js` with a
  `type` of `choice`, `fill` or `cloze`; there is no Q/P split and no
  old-vs-new bank distinction. All inputs are plain JSON in `mth028/data/` and
  the builder is `mth028/build/assemble_bank.py`. To add questions or topics
  later: add the crop under `mth028/out/img/q/` (copy it into the site's `img/q/`),
  add a row to the relevant JSON, then rebuild — **no page code changes**:

  ```bash
  python3 mth028/build/assemble_bank.py --out bank.js
  ```

  Counts, chapter ids, topic ids and blank counts are all read from data;
  nothing is hardcoded. `mth028/build/make_app.py` is a compatibility wrapper
  for the same builder. `mth028/data/topic_map_overrides.json` holds 22
  hand-audited topic corrections that win over the keyword classifier.
- **Pipeline (v2, 30 PDFs).** `build/extract_v2.py` reads the 30 review exports
  → `data/extract_v2.json`; `build/select_items.py` decides answer keys, merges
  duplicate templates and writes `data/selection.json` + `data/duplicates.json`;
  `build/render_crops.py` renders the two images per item; `build/map_topics_v2.py`
  assigns a section; `build/classify_subtopics.py` assigns the sub-topic;
  `build/merge_bank.py` writes the four files the assembler consumes. Re-run them in that order, then
  `assemble_bank.py --out ../mth026/repo/bank.js`.
- **Sources.** The 285 items come from **45** Moodle *attempt review* exports in
  three folders — `MTH028-Quizzes/1.pdf … 15.pdf` (prefix `Q`), `题库2/2-1.pdf …
  2-15.pdf` (prefix `B`) and `HJT/3-1.pdf … 3-15.pdf` (prefix `H`) — 15
  questions each, **675 raw records**.
- **Templates vs records.** Moodle re-draws the numbers for every attempt, so
  the same *template* comes back with different matrices. **Not one pair of the
  675 records is byte-identical** — so this is not de-duplication in the usual
  sense: 116 templates account for 506 records (the biggest, Q6-10, appears 19
  times), and the 390 remaining records are the same template re-drawn.
- **Both layers ship.** `bank.js` carries all **675 records**; the 285 that
  carry a printed answer are the *representatives* (`variantOf: null`) and the
  other 390 point at their template via `variantOf` (list:
  `mth028/data/duplicates.json`). The page lists, counts, schedules and grades
  by template (`MAIN` = the 285), and folds the other draws under the card as
  「同模板的另外 N 组数字」 — one click opens that draw and grades it on its own
  numbers. 89 of the 390 have no printed answer at all and open in self-check
  mode (chips are dashed and say 自评).
- **Two-level index (二级目录).** Every item also carries `sub`, a subtopic id
  taken from the midterm handout (`MTH028 线代期中自学课件.pdf`, 12 modules /
  ~31 考点): 26 sub-topics under the 17 textbook sections, 25 of them in use.
  `mth028/data/subtopics.json` is the list, `subtopic_rules.json` the classifier
  (regex → subtopic, weighted), `subtopic_overrides.json` the human fixes,
  `subtopic_map.json` the result and `subtopic_report.txt` what moved.
  An item's **section is derived from its subtopic**, so the classifier also
  repaired the first level (linear independence had been filed under 1.1).
- **Numbering.** Labels are now positions, not sources: `1.2.3-04` = section 1.2,
  sub-topic 1.2.3, 4th question there. The old `Q1-01` / `B…` / `H…` label is
  kept as `src` (hover text, admin console, this repo's cross-references). A
  variant is `1.5.1-02-v3` — it has no position of its own.
- **Data files.** `selection.json` = the 285 representatives;
  `selection_all.json` = all 675 (this is what renders the images, what
  `merge_bank.py` reads and what the admin console indexes). Question
  crops live in `img/q/<qid>.png`, printed answer crops in `img/a/<qid>.png`.
- **Cropping (why it cannot leak).** Every card in those exports is a drawn
  rounded rectangle with a fixed border colour, so the crop is the **exact stem
  card** and the answer crop is the **exact feedback card** — no heuristic "stop
  before the verdict" line any more. Inside the stem card the renderer only
  whitewashes what a student must not see before answering: the radio buttons
  (redrawn as empty ones), the tick/cross glyphs, and any value typed into an
  answer box (redrawn as an empty box). The feedback card is never part of the
  question image, which is what used to slice the worked solution into the
  screenshot.
- **Answer keys.** 228 choice items all carry a letter: 24 from the Moodle tick,
  the rest by matching the printed answer box against the options (exact /
  containment / digit-multiset); the 29 that stayed ambiguous were re-read from
  the rendered answer box and, where that disagreed, corrected —
  `mth028/data/answer_fixes.json` records every such key. 43 fill items grade
  from the printed answer line, 14 multi-blank items (`cloze`, 2 or 4 blanks)
  grade blank by blank. **13 items printed no answer at all** — those were
  computed and verified with sympy, flagged `答案由 AI 生成 / AI-generated
  answer`, and listed in `MTH028_AI_Answers.md`.
- **Answers.** 56 of the 100 choice items have a reliable letter (19 from the
  Moodle tick, 37 from an exact text match against the printed answer); the
  other 44 show the printed-answer crop and ask you to self-mark. 45 fill/cloze
  items grade automatically; 5 matrix/vector answers self-mark. **30 items had
  no printed answer at all** — their answers were computed independently and are
  flagged `答案由 AI 生成 / AI-generated answer` in the UI. The full list with
  question numbers, working and confidence is `MTH028_AI_Answers.md`.
- **Topic coverage.** The slides cover 1.1–1.5, 1.7–1.9, 2.1–2.4 and 2.8.
  Sections 1.6, 2.5, 2.6 and 2.7 have no slides; they are still listed with a
  textbook title and marked 「课件暂缺」. Quiz 3 (exports 11–15 and 题库2 2-11…2-15)
  brought chapter-2 material, so the bank now fills 2.1 (matrix operations),
  2.2 (inverses), 2.3 (invertibility) and 2.8 (null space / col A); 1.6, 2.4–2.7
  still show 「暂无题目 · 待补充」 rather than a fake 0/0 bar.
- **Glossary.** 212 English/Chinese terms with short definitions, taken from
  the department's *Vocabulary Booklet for Linear Algebra*.

The two WeChat reference PDFs (题库分类汇总 / 线代考点梳理) were used only to
check topic categorisation; **none of their questions entered this bank**.

---

## MTH026 — what is in here / 里面有什么

---

## What is in here / 里面有什么

| Part | Count | What it is |
|---|---|---|
| **A · compiled bank** (`q/`) | 351 | Q1–Q351, one PNG per question, taken straight from the source pages |
| **B · your attempts** (`pq/`) | 323 | P1–P323, the items actually served in Practice quiz 1/2/3 (W4 / W6 / W8) |
| **Reference** | 54 + 5 + 80 | method card per topic, 5 formula groups, 80 glossary terms |

Every question, every answer line and every worked solution is a **page crop** —
nothing was retyped, so no fraction, radical or interval can drift in transcription.

### Part A vs Part B

They are not two copies of the same questions. The two sets share templates but
**the numbers are randomised per attempt**: only 2 of the 323 Part-B items are
verbatim identical to a Part-A item, 179 share a template with different numbers,
and the rest are the same template with different parameters. That is why Part B
is worth keeping — it is the paper you actually saw.

Part B carries no answer **letter**. A printed answer such as `Answer: (−6, −2).`
has to be matched against five rendered options, and the text layer of the source
PDFs puts a fraction's numerator and denominator on different baselines, so any
attempt to recover the letter automatically is unreliable (best measured agreement:
16%). Instead the page shows the paper's own answer line and lets you mark your own
attempt — the deck on the home screen is exactly that.

---

## Running it locally / 本地运行

One file, standard library only:

```bash
MTH026_ROOT=$PWD MTH026_DB=/tmp/mth026.db MTH026_PORT=8088 \
  python3 server/server.py
# open http://localhost:8088/
```

Opening `index.html` straight from disk also works, but then there is no server:
the page falls back to guest mode and keeps progress in `localStorage` only.

Progress lives in `localStorage` under `mth026.en.v1` **and**, when signed in, in
SQLite on the server. Reset clears both.

## Using it / 怎么用

- **Practice** — the smart round, one question at a time over all 674 items.
  - **Phase 1 — coverage.** Every topic is served once, in syllabus order. A topic
    counts as *started* when a graded item **or** one of its originals has an answer.
  - **Phase 2 — weakness.** Every topic is scored and the highest wins:
    `5·min(open mistakes, 3)` + `2.2·(1−accuracy)·min(answered, 4)` +
    `1.5·(1−coverage)` + `0.7·min(days since last try, 30)/7`, minus `1.2` for the
    topic served last. Open mistakes dominate, so a finished round always reopens on
    what you got wrong; the anti-repeat term only breaks near-ties.
  - **Inside the winning topic** picks are **randomised, originals first**: an open
    mistake is retested first (originals before compiled), then an unseen original,
    then an unseen compiled item, then one of the three stalest at random. Both
    decks therefore appear every round, with the paper you actually sat leading —
    but the order inside each band is random, so you cannot memorise a sequence.
  - **Rounds.** Each answer marks its topic as seen; when all 54 are seen the round
    counter advances and the next round starts from the error list.
  - **Skip.** *Skip question* (key `S`) hides that item for 12 h, *Skip topic*
    (key `T`) hides the whole topic — both jump straight to the next pick. The home
    screen lists how much is skipped and clears it in one click.
  - The card states **why** it chose that item, in both languages
    ("3 open mistakes in this topic · 这类还有 3 道错题没订正").
- **Topic mastery** measures each topic across both decks: `done/total` counts
  graded **and** originals, the bar is coverage, its colour is accuracy, and
  `n✕` is the number of open mistakes. Clicking a row drills the whole topic,
  graded first.
- **Quiz originals · 10** — the 323 items you were served. **321 now mark
  themselves**: their correct letter was recovered from the paper's own review line
  `The correct answer is:`, matched against the five option blocks by their
  three-line fraction structure (the earlier attempt used the `Answer:` line, which
  is what the *student* wrote — that is why it never matched). The two items nobody
  answered keep the printed-answer crop and self-marking.
- **Reference** — 54 topics × (what it tests · how to do it · the trap), formula
  sheet, terminology; each topic can be drilled as graded-only, originals-only or
  the whole topic.
- **Bank** — all 674 items in one index: filter by compiled/originals and by
  chapter, or jump straight to `Q12`, `P7` or a topic id such as `2.5`.
- **Preview · 题库速览** — the whole bank with the answers **shown immediately**.
  No picking a letter, no scoring, nothing written to your history. Filter by
  compiled / originals / favourites and by chapter, search `12`, `Q12`, `P7` or a
  topic name, then page through six fully expanded cards at a time. A compiled card
  prints `Answer: B` plus a fold-out English/Chinese worked solution; an original
  card shows the printed `Answer:` crop and the printed solution crop. Every card
  can jump straight into `Practice this` when you do want to be tested.
  Deep link `#preview`.
- **Favourites · 收藏** — the star on any question card (or key `F`) bookmarks that
  item. Stars work in the smart round, in topic drills and in the preview cards.
  The bank index shows a ★ marker on starred items, but it is a jump list —
  toggle a star on a question card instead. `#fav` opens the favourites shelf,
  which reuses the preview cards
  so you can revise them with answers visible. The star state syncs with your
  account, and *un-starring* syncs too (a signed timestamp tombstone, so a stale
  device cannot resurrect a removed bookmark).
  Deep link `#fav`.
- **Bilingual** — every module carries Chinese beside the English (topic names,
  card labels, reference headings, the mastery table, the account dialog). English
  stays primary; Chinese never replaces a label.
- Deep links: `#pq`, `#ref`, `#bank`, `#preview`, `#fav`.

## Accounts & sync / 账号与同步

Sign in from the top bar with a username and a password — no email, no
verification. What it buys you is one progress list across devices.

| Endpoint | Purpose |
|---|---|
| `POST /api/register` `{u,p}` | create the account and start a session |
| `POST /api/login` `{u,p}` | sign in on another device |
| `POST /api/logout` | end the session |
| `GET /api/me` | who is signed in, or `null` |
| `GET /api/progress` | this user's records |
| `PUT /api/progress` | merge records, returns the merged set |
| `DELETE /api/progress` | wipe them (the Reset button does this when signed in) |

Merging is **per item, newest timestamp wins**, with `streak`/`best` taking the
maximum. Two devices therefore cannot erase each other's work: each fills in what
the other has not answered, and a re-answer overrides the older attempt.

`fav` is a map of `item id -> signed timestamp`: positive means starred, negative
is a tombstone meaning un-starred, and the larger absolute timestamp wins. That
is what makes removing a favourite propagate instead of being re-added by an
older device. The server whitelists this field in `clean_progress()` and merges it
in `merge()` alongside the answer history. Values that are not signed ms
timestamps (booleans, nulls, unparseable strings, magnitudes above `10^14`) are
dropped, so a malformed or oversized value cannot pin a key forever.

Local storage is partitioned per account. The guest bucket is `mth026.en.v1`; each
account gets `mth026.en.v1@<username>`. Signing in for the first time folds the
guest's records into that account, so work done before registering is not lost.
Switching accounts only swaps buckets and never merges them — account A's answers
and stars can no longer leak into account B, which is what the old single bucket
did.

How it is stored and protected:

* `users` — username (case-insensitive unique), 16-byte salt, PBKDF2-HMAC-SHA256
  digest at 200 000 rounds. Plaintext passwords are never written anywhere.
* `sessions` — a 43-character random token in an `HttpOnly; SameSite=Lax` cookie;
  only its SHA-256 is stored server-side, 30-day expiry, pruned on each login.
* `progress` — one JSON blob per user; the server accepts at most 512 KB and keeps
  only the fields the app actually writes.
* 10 failed logins per IP per 10 minutes, then 429; cross-origin `POST`/`PUT`
  rejected on the `Origin` header; static paths resolved with `realpath` and
  confined to the document root.

Not included, on purpose: password reset by email and HTTPS. The cookie is not
marked `Secure` because the site is served over plain HTTP on :8088 — put nginx
(or Caddy) in front with a certificate before treating this as anything more than
a study aid. Password reset and account deletion exist, but only from the **admin
console** below, not for end users.

## Admin console / 后台管理

<http://183.66.27.19:58621/admin> — a separate page with its own password, its own
cookie and its own audit trail. It is **not** a role in the `users` table: the
password lives in `/opt/mth026/admin.env`, so registering a username called `admin`
grants nothing.

```bash
# on the server, once
printf 'MTH026_ADMIN_PW=%s\n' "$(python3 -c 'import secrets;print(secrets.token_urlsafe(18))')" \
  > /opt/mth026/admin.env
chmod 600 /opt/mth026/admin.env
systemctl restart mth026        # the unit reads it through EnvironmentFile=-
```

Without that file the console is disabled and `/api/admin/*` answers 503 — the
public site is unaffected.

What it shows: users, new today / this week, 7-day active sessions, total answers,
overall accuracy, suspensions, database size, a 14-day registration chart, and a
searchable / sortable user table (`newest`, `recently active`, `most answered`,
`lowest accuracy`, `username`) with per-user answered / correct / accuracy / session
count / last seen.

What it can do — every write is recorded in `audit` (last 2000 kept):

| Action | Effect |
|---|---|
| Reset password | new PBKDF2 hash, **all sessions of that user killed** |
| Clear progress | deletes their progress blob, keeps the account |
| Sign out everywhere | kills sessions without suspending |
| Suspend / lift | login refused with 403 until the date; sessions killed now |
| Delete account | removes user + sessions + progress, irreversible |
| Export CSV | all users with progress roll-ups, BOM so Excel reads UTF-8 |

Admin endpoints, all requiring the `mth026_admin` cookie
(`HttpOnly; SameSite=Strict`, 12 h, stored hashed):

```
POST /api/admin/login {p}      POST /api/admin/logout    GET /api/admin/state
GET  /api/admin/stats          GET  /api/admin/users?q=&sort=&limit=&offset=
GET  /api/admin/audit          GET  /api/admin/export.csv
POST /api/admin/user/pw {id,p}       POST /api/admin/user/reset {id}
POST /api/admin/user/kick {id}       POST /api/admin/user/ban {id,days}   (0 = 10 years)
POST /api/admin/user/unban {id}      POST /api/admin/user/del {id}
```

`/api/health` now returns only `{"ok":true,"port":…}` — it used to leak the user
count to anyone who asked.

### Bank editor / 题库管理

The **Bank 题库** tab lists all 674 items with their built-in answer and the current
one, filterable by compiled / originals and by *changed* / *missing*, searchable by
`Q12`, `P7` or a topic id. Editing an answer writes one row to `bank_overrides`; the
app fetches `GET /api/overrides` at boot and patches the in-memory question object,
so **no rebuild of `index.html` is needed**.

```
GET  /api/overrides                                  (public: {v, rows:[{id,a,note}]})
GET  /api/admin/bank?q=&k=&filter=&offset=&limit=
POST /api/admin/bank/ans {id, a}      a = "A".."E", or null to clear
POST /api/admin/bank/note {id, note}
```

Four rules that are easy to get wrong:

- **Clearing an override deletes the row**, restoring the built-in letter.
- **`/api/overrides` only ever returns valid `A`–`E`.** It must never return null:
  assigning null to a compiled item's answer makes `L===q.a` false forever and the
  question unanswerable.
- **History is not recomputed.** An old `ok` is frozen, and neither the local blob
  nor the server stores what the answer was at the time, so a retroactive regrade is
  not possible (and re-stamping timestamps would overwrite other devices).
- **Change the answer, then reload before answering.** A page opened before the
  change still grades with the old letter, and that verdict is permanent. The app
  deliberately does not hot-reload answers mid-round, because repainting a question
  card would erase the picked answer and the revealed solution.

Editing counts as an override only for display and future grading; the built-in
letters come from `build/bank_index.json`, which is also what the console shows as
"original answer".

## Deployment / 部署

Two pieces: the generated site in `/var/www/mth026`, the server in `/opt/mth026`
with its SQLite file next to it.

```bash
rsync -az index.html katex q pq user@host:/var/www/mth026/
ssh user@host 'mkdir -p /opt/mth026/data'
scp server/server.py user@host:/opt/mth026/server.py
scp server/bank_index.json user@host:/opt/mth026/bank_index.json   # 674 built-in answers
scp admin.html user@host:/var/www/mth026/admin.html
scp deploy-mth026.service user@host:/etc/systemd/system/mth026.service
ssh user@host 'systemctl daemon-reload && systemctl enable --now mth026'
```

`deploy-mth026.service` binds `0.0.0.0:8088`; the host maps that to
`183.66.27.19:58621` on its elastic public IP. The service creates the schema on
first start and restarts on failure. Text responses are gzipped (`index.html`
259 KB → 65 KB) and the two crop folders are served `immutable` for 30 days.

## Regenerating / 重新生成

`tools/` holds the generators (`make_app_en.py` builds this page; `make_qbank.py`
and `make_outline.py` build the printable PDFs). They expect the source material —
the compiled bank PDF and the 15 Moodle attempt PDFs — to sit at the paths recorded
at the top of each script, so they are not runnable from this repo alone. The
generated artefacts are committed instead.

```
tools/quiz_parse.py      attempt PDFs -> blocks -> items, template-matched to topics
tools/export_pcrops.py   three crops per item (question / answer line / solution)
tools/pb.py              renders the Part-B block for one topic
tools/make_app_en.py     this page
```

---

*Content © the original author of the MTH026 materials; this repository is a
private study aid.*
