#!/usr/bin/env python3
"""MTH026 question bank: static site + a small account / progress API.

Standard library only, so the box needs nothing but python3.  It replaces
`python3 -m http.server` on the same port and adds four ideas:

  * accounts      username + password, PBKDF2-HMAC-SHA256, 200k rounds
  * sessions      random token in an HttpOnly, SameSite=Lax cookie
  * progress      one JSON blob per user, merged per item by timestamp
  * sane static   path-traversal guard, gzip, long cache on the crop folders

Env:
  MTH026_ROOT   document root           (default /var/www/mth026)
  MTH026_DB     sqlite file             (default /opt/mth026/data/app.db)
  MTH026_PORT   listen port             (default 8088)
"""

import csv
import gzip
import hashlib
import hmac
import io
import json
import mimetypes
import os
import re
import secrets
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

ROOT = os.path.realpath(os.environ.get("MTH026_ROOT", "/var/www/mth026"))
DB_PATH = os.environ.get("MTH026_DB", "/opt/mth026/data/app.db")
PORT = int(os.environ.get("MTH026_PORT", "8088"))
ADMIN_PW = os.environ.get("MTH026_ADMIN_PW", "").strip()

COOKIE = "mth026_sid"
ADMIN_COOKIE = "mth026_admin"
ADMIN_SESSION_SECS = 12 * 3600
SESSION_SECS = 30 * 24 * 3600
MAX_BODY = 512 * 1024          # 674 items with metadata stay well under this
PBKDF2_ROUNDS = 200_000
MIN_PW, MAX_PW = 6, 72
NAME_RE = re.compile(r"^[A-Za-z0-9_.\-]{3,24}$")
MAX_ITEMS = 900

LOCK = threading.Lock()

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".mjs": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".ico": "image/x-icon",
    ".woff": "font/woff",
    ".woff2": "font/woff2",
    ".ttf": "font/ttf",
    ".pdf": "application/pdf",
    ".txt": "text/plain; charset=utf-8",
}
COMPRESSIBLE = (".html", ".css", ".js", ".json", ".svg", ".txt")

# login throttling, per client ip: 10 failures inside 10 minutes
FAILS = {}
FAIL_WINDOW = 600
FAIL_LIMIT = 10


# ---------------------------------------------------------------- database
def connect():
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    con = connect()
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS users(
            id      INTEGER PRIMARY KEY,
            name    TEXT UNIQUE NOT NULL,
            display TEXT NOT NULL,
            salt    BLOB NOT NULL,
            hash    BLOB NOT NULL,
            created REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions(
            token   TEXT PRIMARY KEY,
            uid     INTEGER NOT NULL,
            created REAL NOT NULL,
            seen    REAL NOT NULL,
            ip      TEXT
        );
        CREATE TABLE IF NOT EXISTS progress(
            uid     INTEGER PRIMARY KEY,
            blob    TEXT NOT NULL,
            updated REAL NOT NULL
        );
        CREATE TABLE IF NOT EXISTS admin_sessions(
            token   TEXT PRIMARY KEY,
            created REAL NOT NULL,
            seen    REAL NOT NULL,
            ip      TEXT
        );
        CREATE TABLE IF NOT EXISTS audit(
            id      INTEGER PRIMARY KEY,
            ts      REAL NOT NULL,
            ip      TEXT,
            action  TEXT NOT NULL,
            target  TEXT,
            detail  TEXT
        );
        CREATE INDEX IF NOT EXISTS sessions_uid ON sessions(uid);
        CREATE INDEX IF NOT EXISTS audit_ts ON audit(ts);
        """
    )
    cols = {r["name"] for r in con.execute("PRAGMA table_info(users)")}
    if "banned" not in cols:                      # suspension: epoch until which
        con.execute("ALTER TABLE users ADD COLUMN banned REAL NOT NULL DEFAULT 0")
    con.commit()
    con.close()


def audit(ip, action, target, detail=""):
    """Append one line to the admin audit trail, trimmed to the last 2000."""
    con = connect()
    try:
        con.execute(
            "INSERT INTO audit(ts, ip, action, target, detail) VALUES(?,?,?,?,?)",
            (time.time(), ip, action, str(target)[:64], str(detail)[:300]),
        )
        con.execute("DELETE FROM audit WHERE id <= (SELECT MAX(id) - 2000 FROM audit)")
        con.commit()
    finally:
        con.close()


def hash_pw(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ROUNDS)


def token_key(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- progress
def _fav_int(v):
    """Normalise one fav value to a signed int; None means skip this item.

    Only signed millisecond timestamps are kept.  booleans/None, unparseable
    values and out-of-range magnitudes are dropped so one device cannot pin a
    key forever or create a ghost favourite.
    """
    if isinstance(v, bool) or v is None:
        return None
    try:
        n = int(v)
    except (TypeError, ValueError, OverflowError):
        return None
    return n if abs(n) <= 10**14 else None


def _h_ts(rec):
    """Tolerate junk/Infinity h timestamps (historical blobs); default 0."""
    try:
        return int(float((rec or {}).get("t") or 0))
    except (TypeError, ValueError, OverflowError, AttributeError):
        return 0


def clean_progress(payload):
    """Keep only the shape the app actually writes."""
    if not isinstance(payload, dict):
        payload = {}
    out = {"h": {}, "streak": 0, "best": 0, "fav": {}}
    raw = payload.get("h")
    if isinstance(raw, dict):
        for k, v in list(raw.items())[:MAX_ITEMS]:
            try:
                key = str(int(k))
            except (TypeError, ValueError):
                continue
            if not isinstance(v, dict):
                continue
            letter = v.get("a")
            letter = letter if isinstance(letter, str) and len(letter) == 1 else None
            ts = _h_ts(v)
            rec = {"a": letter, "ok": bool(v.get("ok")), "t": ts}
            if v.get("self"):
                rec["self"] = 1
            out["h"][key] = rec
    raw_fav = payload.get("fav")
    if isinstance(raw_fav, dict):
        for k, v in list(raw_fav.items())[:MAX_ITEMS]:
            try:
                key = str(int(k))
            except (TypeError, ValueError):
                continue
            val = _fav_int(v)
            if val is None:
                continue
            out["fav"][key] = val
    for field in ("streak", "best"):
        try:
            out[field] = max(0, int(payload.get(field) or 0))
        except (TypeError, ValueError):
            out[field] = 0
    return out


def merge(old, new):
    """Per-item last write wins, so two devices never erase each other."""
    out = {"h": {}, "streak": 0, "best": 0, "fav": {}}
    for src in (old or {}, new or {}):
        for k, v in (src.get("h") or {}).items():
            prev = out["h"].get(k)
            if prev is None or _h_ts(v) >= _h_ts(prev):
                out["h"][k] = v
        for field in ("streak", "best"):
            try:
                out[field] = max(out[field], int(src.get(field) or 0))
            except (TypeError, ValueError):
                pass
        fav = src.get("fav") or {}
        if isinstance(fav, dict):
            for k, v in list(fav.items())[:MAX_ITEMS]:
                try:
                    key = str(int(k))
                except (TypeError, ValueError):
                    continue
                val = _fav_int(v)
                if val is None:
                    continue
                cur = out["fav"].get(key)
                if cur is None or abs(val) >= abs(cur):
                    out["fav"][key] = val
    return out


# ------------------------------------------------------------- rate limit
def client_ip(handler):
    fwd = handler.headers.get("X-Forwarded-For")
    if fwd:
        return fwd.split(",")[0].strip()
    return handler.client_address[0]


def too_many(ip):
    now = time.time()
    with LOCK:
        hits = [t for t in FAILS.get(ip, []) if now - t < FAIL_WINDOW]
        FAILS[ip] = hits
        return len(hits) >= FAIL_LIMIT


def note_fail(ip):
    with LOCK:
        FAILS.setdefault(ip, []).append(time.time())


def clear_fail(ip):
    with LOCK:
        FAILS.pop(ip, None)


# ---------------------------------------------------------------- handler
class App(BaseHTTPRequestHandler):
    server_version = "mth026/1.0"
    protocol_version = "HTTP/1.1"
    timeout = 30

    # ---- plumbing
    def log_message(self, fmt, *args):
        if self.path.startswith("/api/"):
            super().log_message(fmt, *args)

    def _send(self, status, body=b"", ctype=None, extra=None, head_only=False):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(status)
        if ctype:
            self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        for k, v in (extra or []):
            self.send_header(k, v)
        self.end_headers()
        if body and not head_only:
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def _json(self, status, obj, extra=None, head_only=False):
        body = json.dumps(obj, separators=(",", ":")).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8", extra, head_only)

    def _err(self, status, msg):
        self._json(status, {"error": msg})

    def _body(self):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            n = 0
        if n <= 0:
            return {}
        if n > MAX_BODY:
            raise ValueError("too big")
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}

    # ---- auth
    def _cookie_token(self):
        for part in (self.headers.get("Cookie") or "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == COOKIE and v:
                return v
        return None

    def _user(self):
        token = self._cookie_token()
        if not token:
            return None
        key = token_key(token)
        con = connect()
        try:
            row = con.execute(
                "SELECT u.id, u.name, u.display, u.created, u.banned FROM sessions s "
                "JOIN users u ON u.id = s.uid WHERE s.token = ?", (key,)
            ).fetchone()
            if not row:
                return None
            if row["banned"] and row["banned"] > time.time():
                return None                       # suspended mid-session
            con.execute("UPDATE sessions SET seen = ? WHERE token = ?", (time.time(), key))
            con.commit()
            return row
        finally:
            con.close()

    def _start_session(self, uid):
        token = secrets.token_urlsafe(32)
        now = time.time()
        con = connect()
        try:
            con.execute(
                "INSERT INTO sessions(token, uid, created, seen, ip) VALUES(?,?,?,?,?)",
                (token_key(token), uid, now, now, client_ip(self)),
            )
            con.execute("DELETE FROM sessions WHERE seen < ?", (now - SESSION_SECS,))
            con.commit()
        finally:
            con.close()
        return token

    def _origin_ok(self):
        """Cheap CSRF belt: a browser sends Origin on cross-site POST/PUT."""
        origin = self.headers.get("Origin")
        if not origin:
            return True
        host = (self.headers.get("Host") or "").strip()
        try:
            return urlsplit(origin).netloc.lower() == host.lower()
        except ValueError:
            return False

    # ---- routing
    def do_GET(self):
        self._route("GET", head_only=False)

    def do_HEAD(self):
        self._route("GET", head_only=True)

    def do_POST(self):
        self._route("POST")

    def do_PUT(self):
        self._route("PUT")

    def do_DELETE(self):
        self._route("DELETE")

    def do_OPTIONS(self):
        self._send(204, b"", None)

    def _route(self, method, head_only=False):
        path = unquote(urlsplit(self.path).path)
        if path.startswith("/api/"):
            try:
                self._api(method, path)
            except ValueError:
                self._err(413, "request too large")
            except Exception:                     # never leak a traceback
                self.log_message("api error on %s", path)
                self._err(500, "server error")
            return
        if method != "GET":
            self._err(405, "method not allowed")
            return
        self._static(path, head_only)

    # ---- api
    def _api(self, method, path):
        api = path[4:].strip("/")
        if method != "GET" and not self._origin_ok():
            return self._err(403, "bad origin")

        if api == "health":
            return self._json(200, {"ok": True, "port": PORT})

        if api == "admin" or api.startswith("admin/"):
            return self._admin(method, path)

        if api == "me":
            row = self._user()
            if not row:
                return self._json(200, {"user": None})
            return self._json(200, {"user": {"name": row["name"], "display": row["display"],
                                            "created": int(row["created"])}})

        if api == "register" and method == "POST":
            return self._register()

        if api == "login" and method == "POST":
            return self._login()

        if api == "logout" and method == "POST":
            return self._logout()

        if api == "progress":
            row = self._user()
            if not row:
                return self._err(401, "not signed in")
            if method == "GET":
                return self._get_progress(row["id"])
            if method == "PUT":
                return self._put_progress(row["id"])
            if method == "DELETE":
                con = connect()
                try:
                    con.execute("DELETE FROM progress WHERE uid = ?", (row["id"],))
                    con.commit()
                finally:
                    con.close()
                return self._json(200, {"h": {}, "streak": 0, "best": 0, "fav": {}, "updated": 0})

        return self._err(404, "no such endpoint")

    def _register(self):
        ip = client_ip(self)
        if too_many(ip):
            return self._err(429, "too many attempts, wait a few minutes")
        data = self._body()
        name = str(data.get("u") or "").strip()
        pw = str(data.get("p") or "")
        if not NAME_RE.match(name):
            return self._err(400, "username must be 3-24 characters: letters, digits, . _ -")
        if not MIN_PW <= len(pw) <= MAX_PW:
            return self._err(400, "password must be 6-72 characters")
        salt = secrets.token_bytes(16)
        digest = hash_pw(pw, salt)
        now = time.time()
        con = connect()
        try:
            try:
                cur = con.execute(
                    "INSERT INTO users(name, display, salt, hash, created) VALUES(?,?,?,?,?)",
                    (name.lower(), name, salt, digest, now),
                )
            except sqlite3.IntegrityError:
                return self._err(409, "that username is taken")
            uid = cur.lastrowid
            con.commit()
        finally:
            con.close()
        clear_fail(ip)
        token = self._start_session(uid)
        self._json(200, {"user": {"name": name.lower(), "display": name, "created": int(now)}},
                   extra=[("Set-Cookie", self._cookie_header(token))])

    def _login(self):
        ip = client_ip(self)
        if too_many(ip):
            return self._err(429, "too many attempts, wait a few minutes")
        data = self._body()
        name = str(data.get("u") or "").strip().lower()
        pw = str(data.get("p") or "")
        con = connect()
        try:
            row = con.execute(
                "SELECT id, name, display, salt, hash, created, banned FROM users WHERE name = ?",
                (name,)).fetchone()
        finally:
            con.close()
        if not row or not hmac.compare_digest(hash_pw(pw, row["salt"]), row["hash"]):
            note_fail(ip)
            return self._err(401, "wrong username or password")
        if row["banned"] and row["banned"] > time.time():
            note_fail(ip)
            return self._err(403, "this account is suspended")
        clear_fail(ip)
        token = self._start_session(row["id"])
        self._json(200, {"user": {"name": row["name"], "display": row["display"],
                                  "created": int(row["created"])}},
                   extra=[("Set-Cookie", self._cookie_header(token))])

    def _logout(self):
        token = self._cookie_token()
        if token:
            con = connect()
            try:
                con.execute("DELETE FROM sessions WHERE token = ?", (token_key(token),))
                con.commit()
            finally:
                con.close()
        self._json(200, {"ok": True},
                   extra=[("Set-Cookie", "%s=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0" % COOKIE)])

    def _cookie_header(self, token):
        return "%s=%s; Path=/; HttpOnly; SameSite=Lax; Max-Age=%d" % (COOKIE, token, SESSION_SECS)

    def _get_progress(self, uid):
        con = connect()
        try:
            row = con.execute("SELECT blob, updated FROM progress WHERE uid = ?", (uid,)).fetchone()
        finally:
            con.close()
        if not row:
            return self._json(200, {"h": {}, "streak": 0, "best": 0, "fav": {}, "updated": 0})
        try:
            data = json.loads(row["blob"])
        except json.JSONDecodeError:
            data = {}
        if not isinstance(data, dict):
            data = {}
        data.setdefault("h", {})
        data.setdefault("streak", 0)
        data.setdefault("best", 0)
        data.setdefault("fav", {})
        data["updated"] = int(row["updated"])
        return self._json(200, data)

    def _put_progress(self, uid):
        incoming = clean_progress(self._body())
        con = connect()
        try:
            row = con.execute("SELECT blob FROM progress WHERE uid = ?", (uid,)).fetchone()
            old = None
            if row:
                try:
                    old = json.loads(row["blob"])
                except json.JSONDecodeError:
                    old = None
            merged = merge(old, incoming)
            now = time.time()
            con.execute(
                "INSERT INTO progress(uid, blob, updated) VALUES(?,?,?) "
                "ON CONFLICT(uid) DO UPDATE SET blob = excluded.blob, updated = excluded.updated",
                (uid, json.dumps(merged, separators=(",", ":")), now),
            )
            con.commit()
        finally:
            con.close()
        merged["updated"] = int(now)
        return self._json(200, merged)

    # ---- admin
    def _admin_token(self):
        for part in (self.headers.get("Cookie") or "").split(";"):
            k, _, v = part.strip().partition("=")
            if k == ADMIN_COOKIE and v:
                return v
        return None

    def _admin_ok(self):
        if not ADMIN_PW:
            return False
        tok = self._admin_token()
        if not tok:
            return False
        key = token_key(tok)
        now = time.time()
        con = connect()
        try:
            row = con.execute("SELECT created FROM admin_sessions WHERE token = ?", (key,)).fetchone()
            if not row:
                return False
            if row["created"] < now - ADMIN_SESSION_SECS:
                con.execute("DELETE FROM admin_sessions WHERE token = ?", (key,))
                con.commit()
                return False
            con.execute("UPDATE admin_sessions SET seen = ? WHERE token = ?", (now, key))
            con.commit()
            return True
        finally:
            con.close()

    def _admin(self, method, path):
        api = path[len("/api/admin"):].strip("/")

        if api == "login" and method == "POST":
            return self._admin_login()
        if api == "logout" and method == "POST":
            return self._admin_logout()
        if api == "state":
            return self._json(200, {"enabled": bool(ADMIN_PW), "signed_in": self._admin_ok()})
        if not self._admin_ok():
            return self._err(401, "admin sign-in required")

        if api == "stats":
            return self._admin_stats()
        if api == "users":
            return self._admin_users()
        if api == "audit":
            return self._admin_audit()
        if api == "export.csv":
            return self._admin_csv()
        if api == "user/pw" and method == "POST":
            return self._admin_pw()
        if api == "user/reset" and method == "POST":
            return self._admin_reset()
        if api == "user/kick" and method == "POST":
            return self._admin_kick()
        if api == "user/ban" and method == "POST":
            return self._admin_ban()
        if api == "user/unban" and method == "POST":
            return self._admin_unban()
        if api == "user/del" and method == "POST":
            return self._admin_del()
        return self._err(404, "no such endpoint")

    def _admin_login(self):
        if not ADMIN_PW:
            return self._err(503, "admin console disabled: set MTH026_ADMIN_PW")
        ip = client_ip(self)
        gate = "admin:" + ip
        if too_many(gate):
            return self._err(429, "too many attempts, wait a few minutes")
        pw = str(self._body().get("p") or "")
        if not hmac.compare_digest(pw.encode("utf-8"), ADMIN_PW.encode("utf-8")):
            note_fail(gate)
            audit(ip, "admin.login.fail", "-", "")
            return self._err(401, "wrong admin password")
        clear_fail(gate)
        tok = secrets.token_urlsafe(32)
        now = time.time()
        con = connect()
        try:
            con.execute("INSERT INTO admin_sessions(token, created, seen, ip) VALUES(?,?,?,?)",
                        (token_key(tok), now, now, ip))
            con.execute("DELETE FROM admin_sessions WHERE seen < ?", (now - ADMIN_SESSION_SECS,))
            con.commit()
        finally:
            con.close()
        audit(ip, "admin.login", "-", "")
        self._json(200, {"ok": True},
                   extra=[("Set-Cookie", "%s=%s; Path=/; HttpOnly; SameSite=Strict; Max-Age=%d"
                                          % (ADMIN_COOKIE, tok, ADMIN_SESSION_SECS))])

    def _admin_logout(self):
        tok = self._admin_token()
        if tok:
            con = connect()
            try:
                con.execute("DELETE FROM admin_sessions WHERE token = ?", (token_key(tok),))
                con.commit()
            finally:
                con.close()
        self._json(200, {"ok": True},
                   extra=[("Set-Cookie", "%s=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0" % ADMIN_COOKIE)])

    # ---- admin: read
    def _admin_stats(self):
        now = time.time()
        day = 86400
        con = connect()
        try:
            users = con.execute("SELECT id, created, banned FROM users").fetchall()
            sess = con.execute("SELECT COUNT(*) c, COUNT(DISTINCT uid) u FROM sessions WHERE seen > ?",
                               (now - 7 * day,)).fetchone()
            all_sess = con.execute("SELECT COUNT(*) c FROM sessions").fetchone()["c"]
            prog = con.execute("SELECT blob, updated FROM progress").fetchall()
            audits = con.execute("SELECT COUNT(*) c FROM audit").fetchone()["c"]
        finally:
            con.close()

        answered = correct = originals = 0
        for r in prog:
            try:
                h = (json.loads(r["blob"]) or {}).get("h") or {}
            except (json.JSONDecodeError, AttributeError):
                h = {}
            answered += len(h)
            correct += sum(1 for v in h.values() if isinstance(v, dict) and v.get("ok"))
            originals += sum(1 for k in h if str(k).isdigit() and int(k) >= 1000)

        # 14 local-day buckets, so "today" matches the box's clock
        today = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(now)), "%Y-%m-%d"))
        regs = []
        for i in range(13, -1, -1):
            start = today - i * day
            regs.append({
                "d": time.strftime("%m-%d", time.localtime(start)),
                "n": sum(1 for u in users if start <= u["created"] < start + day),
            })
        banned = sum(1 for u in users if u["banned"] and u["banned"] > now)

        try:
            db_size = os.path.getsize(DB_PATH)
        except OSError:
            db_size = 0

        self._json(200, {
            "users": len(users),
            "new_today": sum(1 for u in users if u["created"] >= today),
            "new_7d": sum(1 for u in users if u["created"] >= now - 7 * day),
            "active_7d": sess["u"],
            "sessions": all_sess,
            "banned": banned,
            "answered": answered,
            "correct": correct,
            "originals": originals,
            "progress_rows": len(prog),
            "audit": audits,
            "db_bytes": db_size,
            "regs": regs,
            "now": int(now),
        })

    def _admin_audit(self):
        con = connect()
        try:
            rows = con.execute("SELECT ts, ip, action, target, detail FROM audit "
                               "ORDER BY id DESC LIMIT 120").fetchall()
        finally:
            con.close()
        self._json(200, {"rows": [{"t": int(r["ts"]), "ip": r["ip"], "a": r["action"],
                                   "target": r["target"], "d": r["detail"]} for r in rows]})

    def _collect(self):
        """Every user with its roll-up of progress — the console filters in memory."""
        con = connect()
        try:
            rows = con.execute(
                "SELECT u.id, u.name, u.display, u.created, u.banned, p.updated, p.blob, "
                " (SELECT COUNT(*) FROM sessions s WHERE s.uid = u.id) nsess, "
                " (SELECT MAX(s.seen) FROM sessions s WHERE s.uid = u.id) last_seen "
                "FROM users u LEFT JOIN progress p ON p.uid = u.id"
            ).fetchall()
        finally:
            con.close()
        out = []
        for r in rows:
            h = {}
            if r["blob"]:
                try:
                    h = (json.loads(r["blob"]) or {}).get("h") or {}
                except (json.JSONDecodeError, AttributeError):
                    h = {}
            answered = len(h)
            correct = sum(1 for v in h.values() if isinstance(v, dict) and v.get("ok"))
            out.append({
                "id": r["id"], "name": r["name"], "display": r["display"],
                "created": int(r["created"]), "banned": int(r["banned"] or 0),
                "sessions": r["nsess"], "last": int(r["last_seen"] or 0),
                "updated": int(r["updated"] or 0),
                "answered": answered, "correct": correct,
                "acc": round(correct * 100.0 / answered) if answered else None,
                "originals": sum(1 for k in h if str(k).isdigit() and int(k) >= 1000),
            })
        return out

    def _admin_users(self):
        q = parse_qs(urlsplit(self.path).query)
        needle = (q.get("q") or [""])[0].strip().lower()
        sort = (q.get("sort") or ["new"])[0]
        try:
            limit = max(1, min(int((q.get("limit") or ["50"])[0]), 200))
        except ValueError:
            limit = 50
        try:
            off = max(0, int((q.get("offset") or ["0"])[0]))
        except ValueError:
            off = 0

        rows = self._collect()
        if needle:
            rows = [r for r in rows
                    if needle in r["name"].lower() or needle in (r["display"] or "").lower()
                    or needle == str(r["id"])]
        keys = {
            "new": (lambda r: -r["created"]),
            "old": (lambda r: r["created"]),
            "name": (lambda r: r["name"]),
            "answered": (lambda r: -r["answered"]),
            "active": (lambda r: -r["last"]),
            "worst": (lambda r: (r["acc"] if r["acc"] is not None else 999, -r["answered"])),
        }
        rows.sort(key=keys.get(sort, keys["new"]))
        self._json(200, {"total": len(rows), "offset": off, "limit": limit,
                         "rows": rows[off:off + limit]})

    def _admin_csv(self):
        rows = sorted(self._collect(), key=lambda r: r["created"])
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["id", "username", "display", "registered", "last_seen", "sessions",
                    "answered", "correct", "accuracy_pct", "originals", "progress_updated",
                    "banned_until"])
        fmt = lambda t: time.strftime("%Y-%m-%d %H:%M", time.localtime(t)) if t else ""
        for r in rows:
            w.writerow([r["id"], r["name"], r["display"], fmt(r["created"]), fmt(r["last"]),
                        r["sessions"], r["answered"], r["correct"],
                        "" if r["acc"] is None else r["acc"], r["originals"],
                        fmt(r["updated"]), fmt(r["banned"])])
        body = buf.getvalue().encode("utf-8-sig")     # BOM so Excel reads UTF-8
        audit(client_ip(self), "admin.export", "users", "%d rows" % len(rows))
        self._send(200, body, "text/csv; charset=utf-8",
                   [("Content-Disposition", 'attachment; filename="mth026-users.csv"')])

    # ---- admin: writes
    def _target_id(self, data):
        try:
            return int(data.get("id"))
        except (TypeError, ValueError):
            return None

    def _admin_pw(self):
        data = self._body()
        uid = self._target_id(data)
        pw = str(data.get("p") or "")
        if uid is None:
            return self._err(400, "missing id")
        if not MIN_PW <= len(pw) <= MAX_PW:
            return self._err(400, "password must be 6-72 characters")
        salt = secrets.token_bytes(16)
        con = connect()
        try:
            cur = con.execute("UPDATE users SET salt = ?, hash = ? WHERE id = ?",
                              (salt, hash_pw(pw, salt), uid))
            if cur.rowcount == 0:
                return self._err(404, "no such user")
            con.execute("DELETE FROM sessions WHERE uid = ?", (uid,))
            con.commit()
        finally:
            con.close()
        audit(client_ip(self), "user.password", str(uid), "reset, sessions cleared")
        self._json(200, {"ok": True})

    def _admin_reset(self):
        uid = self._target_id(self._body())
        if uid is None:
            return self._err(400, "missing id")
        con = connect()
        try:
            con.execute("DELETE FROM progress WHERE uid = ?", (uid,))
            con.commit()
        finally:
            con.close()
        audit(client_ip(self), "user.progress.clear", str(uid), "")
        self._json(200, {"ok": True})

    def _admin_kick(self):
        uid = self._target_id(self._body())
        if uid is None:
            return self._err(400, "missing id")
        con = connect()
        try:
            cur = con.execute("DELETE FROM sessions WHERE uid = ?", (uid,))
            n = cur.rowcount
            con.commit()
        finally:
            con.close()
        audit(client_ip(self), "user.signout", str(uid), "%d sessions" % n)
        self._json(200, {"ok": True, "cleared": n})

    def _admin_ban(self):
        data = self._body()
        uid = self._target_id(data)
        if uid is None:
            return self._err(400, "missing id")
        try:
            days = int(data.get("days") or 0)
        except (TypeError, ValueError):
            days = 0
        days = max(0, min(days, 3650))
        until = time.time() + (days or 3650) * 86400
        con = connect()
        try:
            cur = con.execute("UPDATE users SET banned = ? WHERE id = ?", (until, uid))
            if cur.rowcount == 0:
                return self._err(404, "no such user")
            con.execute("DELETE FROM sessions WHERE uid = ?", (uid,))
            con.commit()
        finally:
            con.close()
        audit(client_ip(self), "user.ban", str(uid), "%d days" % (days or 3650))
        self._json(200, {"ok": True, "until": int(until)})

    def _admin_unban(self):
        uid = self._target_id(self._body())
        if uid is None:
            return self._err(400, "missing id")
        con = connect()
        try:
            con.execute("UPDATE users SET banned = 0 WHERE id = ?", (uid,))
            con.commit()
        finally:
            con.close()
        audit(client_ip(self), "user.unban", str(uid), "")
        self._json(200, {"ok": True})

    def _admin_del(self):
        data = self._body()
        uid = self._target_id(data)
        if uid is None:
            return self._err(400, "missing id")
        con = connect()
        try:
            row = con.execute("SELECT name FROM users WHERE id = ?", (uid,)).fetchone()
            if not row:
                return self._err(404, "no such user")
            con.execute("DELETE FROM sessions WHERE uid = ?", (uid,))
            con.execute("DELETE FROM progress WHERE uid = ?", (uid,))
            con.execute("DELETE FROM users WHERE id = ?", (uid,))
            con.commit()
        finally:
            con.close()
        audit(client_ip(self), "user.delete", str(uid), row["name"])
        self._json(200, {"ok": True})

    # ---- static
    def _static(self, path, head_only=False):
        if path in ("", "/"):
            path = "/index.html"
        elif path in ("/admin", "/admin/"):
            path = "/admin.html"
        rel = path.lstrip("/")
        full = os.path.realpath(os.path.join(ROOT, rel))
        if not (full == ROOT or full.startswith(ROOT + os.sep)):
            return self._send(403, b"forbidden", "text/plain; charset=utf-8", head_only=head_only)
        if os.path.isdir(full):
            full = os.path.join(full, "index.html")
        if not os.path.isfile(full):
            return self._send(404, b"not found", "text/plain; charset=utf-8", head_only=head_only)

        ext = os.path.splitext(full)[1].lower()
        try:
            st = os.stat(full)
            with open(full, "rb") as fh:
                body = fh.read()
        except OSError:
            return self._send(404, b"not found", "text/plain; charset=utf-8", head_only=head_only)

        ctype = MIME.get(ext) or mimetypes.guess_type(full)[0] or "application/octet-stream"
        etag = '"%x-%x"' % (int(st.st_mtime), st.st_size)

        if path.startswith(("/q/", "/pq/", "/katex/")):
            cache = "public, max-age=2592000, immutable"
        elif ext in (".html",):
            cache = "no-cache"
        else:
            cache = "public, max-age=86400"

        base = [("Cache-Control", cache), ("ETag", etag)]
        if self.headers.get("If-None-Match") == etag:
            return self._send(304, b"", None, base, head_only=True)

        if ext in COMPRESSIBLE and len(body) > 1024 and "gzip" in (self.headers.get("Accept-Encoding") or ""):
            gz = gzip.compress(body, 6)
            if len(gz) < len(body) * 0.92:
                return self._send(200, gz, ctype, base + [("Content-Encoding", "gzip"),
                                                          ("Vary", "Accept-Encoding")], head_only)

        return self._send(200, body, ctype, base, head_only)


def main():
    init_db()
    httpd = ThreadingHTTPServer(("0.0.0.0", PORT), App)
    httpd.daemon_threads = True
    print("mth026 serving %s on 0.0.0.0:%d (db %s)" % (ROOT, PORT, DB_PATH), flush=True)
    print("admin console: %s" % ("/admin (password set)" if ADMIN_PW
                                 else "/admin disabled — set MTH026_ADMIN_PW"), flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
