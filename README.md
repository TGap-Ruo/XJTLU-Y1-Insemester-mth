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

- **Practice** — smart round. Phase 1 walks one question from every topic; phase 2
  re-weights towards whatever you keep missing. Both decks are in the same pool,
  so the round covers all 674 items: a topic counts as *started* when either a
  graded item **or** one of its originals has an answer, and once a topic's
  graded items are used up the engine serves its originals (self-marked, gold `P`
  badge). Accuracy stays graded-only — the originals never dilute the figure the
  engine steers by.
- **Quiz originals · 10** — the 323 items you were served, self-marked against the
  printed answer.
- **Reference** — 54 topics × (what it tests · how to do it · the trap), formula
  sheet, terminology.
- **Bank** — all 674 items in one index: filter by compiled/originals and by
  chapter, or jump straight to `Q12`, `P7` or a topic id such as `2.5`.
- Deep links: `#pq`, `#ref`, `#bank`.

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

Not included, on purpose: password reset by email, account deletion, HTTPS. The
cookie is not marked `Secure` because the site is served over plain HTTP on :8088
— put nginx (or Caddy) in front with a certificate before treating this as
anything more than a study aid.

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
