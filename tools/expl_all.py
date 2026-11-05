# -*- coding: utf-8 -*-
"""Merge all per-chapter solution dicts into one."""
E = {}
for _m in ("expl_1", "expl_2", "expl_3", "expl_4", "expl_5"):
    try:
        mod = __import__(_m)
        E.update(mod.E)
    except ImportError:
        pass
