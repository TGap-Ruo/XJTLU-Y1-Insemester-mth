#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compatibility wrapper — the authoritative builder is assemble_bank.py.

An earlier draft of this file assembled a *placeholder* bank (empty images,
topics and keys) and once silently replaced the real 150-item bank.  To keep a
single source of truth, running this file now simply delegates to
``assemble_bank.py`` with the same command-line arguments.

Rebuild after editing data/*.json or adding crops:

    python3 mth028/build/make_app.py                 # -> mth028/out/bank.js
    python3 mth028/build/make_app.py --out bank.js  # -> site-root bank.js
    python3 mth028/build/assemble_bank.py --out bank.js   # same thing

The page (index.html + app.css) is fully data driven: it reads
window.MTH028_BANK and hardcodes nothing about item / topic / chapter counts
or id ranges.  Adding questions or topics needs no page code changes.
"""
import runpy
import sys
from pathlib import Path

if __name__ == "__main__":
    target = str(Path(__file__).resolve().parent / "assemble_bank.py")
    sys.argv[0] = target
    runpy.run_path(target, run_name="__main__")
