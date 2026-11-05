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

No build step, no dependencies, no network:

```bash
python3 -m http.server 8088 --directory .
# open http://localhost:8088/
```

Progress is stored in `localStorage` under `mth026.en.v1`; Reset clears it.

## Using it / 怎么用

- **Practice** — smart round. Phase 1 walks one question from every topic; phase 2
  re-weights towards whatever you keep missing.
- **Quiz originals · 10** — the 323 items you were served, self-marked against the
  printed answer.
- **Reference** — 54 topics × (what it tests · how to do it · the trap), formula
  sheet, terminology.
- **Bank** — browse Q1–Q351 by chapter, open any item on its own.
- Deep links: `#pq`, `#ref`, `#bank`.

## Deployment / 部署

Static files, served by a systemd unit running Python's `http.server`:

```bash
scp -r . user@host:/var/www/mth026/
scp deploy-mth026.service user@host:/etc/systemd/system/mth026.service
ssh user@host 'systemctl daemon-reload && systemctl enable --now mth026'
```

`deploy-mth026.service` binds `0.0.0.0:8088`; the host maps that to
`183.66.27.19:58621` on its elastic public IP.

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
