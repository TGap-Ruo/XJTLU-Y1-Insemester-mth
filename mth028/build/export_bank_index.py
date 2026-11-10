#!/usr/bin/env python3
"""Export the server-side answer index for MTH028 (`bank_index28.json`).

The site itself only needs `bank.js`, but the admin console talks to the Python
backend, and the backend must know every question's id / type / blanks / base
answer without parsing JavaScript.  It reads that from

    /opt/mth026/bank_index28.json      (path configurable by MTH028_BANK_INDEX)

which is *generated from bank.js* -- never edited by hand.  If it goes stale the
admin panel lists old items, shows dead image paths and rejects edits to new ids
with "no such item".

    python3 build/export_bank_index.py --out ../mth026/repo/bank_index28.json

Shape (keep it stable; the backend indexes it by `id`):

    {"items": [{"id":1001,"qid":"p1-01","type":"fill","topic":"1.1",
                "label":"Q1-01","img":"img/q/p1-01.png",
                "answerImg":"img/a/p1-01.png","answers":["6"],
                "blanks":1,"answerText":"6"}, ...],
     "topics": [ ...the same topic rows bank.js carries (id/ch/en/zh/focus...) ]}
"""
import argparse
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_IN = os.path.join(ROOT, "out", "bank.js")
DEFAULT_OUT = os.path.join(ROOT, "out", "bank_index28.json")


def load_bank(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    i = raw.find("{")
    if i < 0:
        raise SystemExit("bank.js does not contain a JSON object: %s" % path)
    return json.loads(raw[i:].rstrip().rstrip(";"))


def project(item):
    row = {
        "id": item["id"],
        "qid": item.get("qid"),
        "type": item.get("type"),
        "topic": item.get("topic"),
        "label": item.get("label"),
        "img": item.get("img"),
        "answerImg": item.get("answerImg"),
    }
    if item.get("type") == "choice":
        row["key"] = item.get("key")
        row["options"] = item.get("options") or []
        row["answerText"] = item.get("answerText") or ""
    else:
        row["answers"] = item.get("answers") or []
        row["blanks"] = item.get("blanks") or 1
        row["answerText"] = item.get("answerText") or ""
    return row


def main():
    ap = argparse.ArgumentParser(description="export bank_index28.json from bank.js")
    ap.add_argument("--in", dest="src", default=DEFAULT_IN)
    ap.add_argument("--out", dest="dst", default=DEFAULT_OUT)
    a = ap.parse_args()

    bank = load_bank(a.src)
    items = bank.get("items") or []
    doc = {"items": [project(x) for x in items], "topics": bank.get("topics") or []}
    os.makedirs(os.path.dirname(os.path.abspath(a.dst)), exist_ok=True)
    with open(a.dst, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)

    miss = [x for x in doc["items"]
            if (x["type"] == "choice" and not x.get("key"))
            or (x["type"] != "choice" and len(x.get("answers") or []) != (x.get("blanks") or 1))]
    print("wrote %s: %d items, %d topics, %d without a usable answer"
          % (a.dst, len(doc["items"]), len(doc["topics"]), len(miss)))
    if miss:
        print("  " + ", ".join("%s(%s)" % (m["qid"], m["type"]) for m in miss[:10]))


if __name__ == "__main__":
    main()
