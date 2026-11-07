# MTH026 Calculus I — Complete Question Bank & Smart Quiz

XJTLU Year 1, semester 1 · MTH026 Calculus I. One offline page that holds the whole
revision set: **674 items across 54 topics**, the method card for every topic, a
formula sheet and an 80-term bilingual glossary — plus a spaced-repetition quiz
engine on top of it.

**Live:** <http://183.66.27.19:58621/> (server listens on port 8088)

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
  - **Inside the winning topic** the engine re-tests *the exact item you missed*
    first, then something you have never seen, then the stalest item.
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
- **Quiz originals · 10** — the 323 items you were served, self-marked against the
  printed answer.
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

One deliberate limitation: progress is merged, not replaced. On a shared browser,
signing out of account A and into account B keeps A's local records on the device,
and the next push can copy them into B. Progress and favourites are per account on
the server, but the local cache is not partitioned by account.

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

## Deployment / 部署

Two pieces: the generated site in `/var/www/mth026`, the server in `/opt/mth026`
with its SQLite file next to it.

```bash
rsync -az index.html katex q pq user@host:/var/www/mth026/
ssh user@host 'mkdir -p /opt/mth026/data'
scp server/server.py user@host:/opt/mth026/server.py
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
