from __future__ import annotations

import base64
import hashlib
import hmac
import json
import mimetypes
import os
import random
import sys
import time
import uuid
from pathlib import Path
from urllib.parse import quote

import requests

# ============================================================
#  الجلسة — @lwky460574  |  uid 2039163018882244609
#  auth=Bearer (مسار الويب) جاهز ومفعل
# ============================================================
UID = "2039163018882244609"
SCREEN_NAME = os.environ.get("X_SCREEN_NAME", "lwky460574")

BEARER = os.environ.get(
    "X_BEARER",
    "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
)
# الكوكيز الجديدة
AUTH_TOKEN = os.environ.get("X_AUTH_TOKEN", "49909fd442a1752d65960ac4a91b55b280d531ce")
CT0 = os.environ.get(
    "X_CT0",
    "182ffc69f84cfd5f24bbe7b5f39b4314402faef936ce9d333a9124e2297067c41de60b044aa6a21b42352b34f47eda6f54c0a88f0b34d7457e2255af952b5fcc2a38dcb4ef133921b1ac7293b34f0e85",
)

# OAuth1 (للاحتياط فقط في حال جلبت الـ secret لاحقاً)
CONSUMER_KEY = os.environ.get("X_CONSUMER_KEY", "3nVuSoBZnx6U4vzUxf5w")
CONSUMER_SECRET = os.environ.get("X_CONSUMER_SECRET", "Bcs59dsQ8m3c9C9MvyMkCbLqBhCw7tW")
OAUTH_TOKEN = os.environ.get(
    "X_OAUTH_TOKEN", "2039163018882244609-24NL3QTTXrUrcrd2xCxFMQj9PiKzHR"
)
OAUTH_TOKEN_SECRET = os.environ.get("X_TOKEN_SECRET", "")
USE_OAUTH1 = bool(OAUTH_TOKEN_SECRET)

DEVICE = {
    "trusted-device-id": "2bff31e1-e124-42b1-a307-21aa978412b3",
    "x-client-uuid": "9169c7fc-668d-4ca6-935e-e49d83c1837f",
    "x-twitter-client-deviceid": "76124aa8f45ea297",
    "x-twitter-client-adid": "40801385-7633-4d2f-8bbf-b6cec855a1f2",
    "x-twitter-api-version": "5",
    "x-twitter-client": "TwitterAndroid",
    "x-twitter-client-flavor": "beta",
    "x-twitter-client-version": "12.44.0-prod.01",
    "x-twitter-client-language": "ar-IQ",
    "x-twitter-client-limit-ad-tracking": "0",
    "accept-language": "ar-IQ",
    "x-twitter-active-user": "yes",
    "user-agent": (
        "TwitterAndroid/12.44.0-prod.01 (312440001-r-01) RMX3636/15 "
        "(realme;RMX3636;realme;RMX3636;0;;1;2015)"
    ),
    "x-attest-token": (
        "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJvcyI6ICJBTkRST0lEIiwKImFjY291bnRJZCI6ICIyMDM5MTYz"
        "MDE4ODgyMjQ0NjA5IiwKInZlcnNpb25OdW1iZXIiOiAiMTIuNDQuMCIsCiJvc1ZlcnNpb25OdW1iZXIiOiAiUk1Y"
        "MzYzNi8xNS4iLAoib3NQbGF0Zm9ybSI6ICJUd2l0dGVyQW5kcm9pZCIsCiJkZXZpY2VNb2RlbCI6ICJSTVgzNjM2"
        "IiwKImNsaWVudElkZW50aWZpZXIiOiAiOTE2OWM3ZmMtNjY4ZC00Y2E2LTkzNWUtZTQ5ZDgzYzE4MzdmIiwKImtl"
        "eUlkIjogIk9URTJPV00zWm1NdE5qWTRaQzAwWTJFMkxUa3pOV1V0WlRRNVpEZ3pZekU0TXpkbUxUSXdNemt4TmpN"
        "d01UZzRPREl5TkRRMk1Eaz0iLAoicHVibGljS2V5IjogIk1Ga3dFd1lIS29aSXpqMENBUVlJS29aSXpqMERBUWNE"
        "UWdBRU5XYzV1M0hPWFB4MFpLZ3g5UXI2Qkg1c0ptL2N4Y3lkcWRETFF4bFdZVzAzYWk2V0hnU3JGQTMyUFIralF5"
        "UnN3M1RxN2hiL1ZmYnlsem5xNGFIaG53PT0iLAoiZXhwaXJlc0F0IjogIjE3OTUwNTYwMTM1NDQifQ.9NGEHSYzzHRyeY7CMBKwBveyWyQiAs-VAcYyNzI95SE"
    ),
}

WEB_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

OP_CREATE_POST = os.environ.get("X_OP_CREATE", "2kRHOWtGNeMkV69EVVlChA")

CREATE_FEATURES = {
    "android_ui_nested_quote_tweet_preview_enabled": False,
    "grok_translations_community_note_auto_translation_is_enabled": False,
    "grok_translations_community_note_translation_is_enabled": False,
    "grok_translations_post_auto_translation_is_enabled": False,
    "immersive_video_status_linkable_timestamps": True,
    "subscriptions_feature_can_gift_premium": False,
    "x_lite_quick_promote_analytics_banner_enabled": False,
    "x_sports_post_context_enabled": True,
}

CHUNK_VIDEO = 4 * 1024 * 1024
MEDIA_CATEGORY = os.environ.get("MEDIA_CATEGORY", "amplify_video")

# مسار الرفع يتحدد حسب نوع الجلسة
UPLOAD_APP = "https://upload.x.com/1.1/media/upload2.json"
UPLOAD_WEB = "https://upload.twitter.com/i/media/upload.json"
_upload_url = [UPLOAD_APP if USE_OAUTH1 else UPLOAD_WEB]

DB_FILE = Path(os.environ.get(
    "DB_PATH",
    "3dgoon_db.json",
))

BASE_DIR = DB_FILE.parent
POSTED_FILE = BASE_DIR / "posted.json"
STATE_FILE = BASE_DIR / "post_state.json"
LOG_FILE = BASE_DIR / "autoposter.log"


# ---------------- Logging ----------------
def log(msg: str) -> None:
    line = "[%s] %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    try:
        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


# ---------------- OAuth1 ----------------
def _pct(v) -> str:
    return quote(str(v), safe="-._~")


def oauth1_header(method: str, url: str, params: dict | None = None) -> str:
    oauth = {
        "oauth_consumer_key": CONSUMER_KEY,
        "oauth_nonce": str(random.randint(10 ** 34, 10 ** 35 - 1)),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": OAUTH_TOKEN,
        "oauth_version": "1.0",
    }
    all_params = {**(params or {}), **oauth}
    pairs = sorted((_pct(k), _pct(v)) for k, v in all_params.items())
    norm = "&".join(f"{k}={v}" for k, v in pairs)
    base = "&".join([method.upper(), _pct(url.split("?", 1)[0]), _pct(norm)])
    key = f"{_pct(CONSUMER_SECRET)}&{_pct(OAUTH_TOKEN_SECRET)}"
    sig = base64.b64encode(
        hmac.new(key.encode(), base.encode(), hashlib.sha1).digest()
    ).decode()
    parts = {"realm": "https://api.twitter.com/", **oauth, "oauth_signature": sig}
    return "OAuth " + ", ".join(f'{k}="{_pct(v)}"' for k, v in parts.items())


# ---------------- HTTP ----------------
def app_headers(extra: dict | None = None) -> dict:
    h = {"accept": "*/*", **DEVICE}
    if extra:
        h.update(extra)
    return h


def web_headers(extra: dict | None = None) -> dict:
    h = {
        "User-Agent": WEB_UA,
        "Accept": "*/*",
        "Accept-Language": "ar",
        "authorization": f"Bearer {BEARER}",
        "x-csrf-token": CT0,
        "x-twitter-auth-type": "OAuth2Session",
        "x-twitter-active-user": "yes",
        "x-twitter-client-language": "ar",
        "x-client-uuid": DEVICE["x-client-uuid"],
        "trusted-device-id": DEVICE["trusted-device-id"],
        "Cookie": f"auth_token={AUTH_TOKEN}; ct0={CT0}; twid=u%3D{UID}; lang=ar",
        "referer": "https://x.com/",
        "origin": "https://x.com",
    }
    if extra:
        h.update(extra)
    return h


def auth_for(method: str, url: str, params: dict | None = None,
             extra: dict | None = None) -> dict:
    if USE_OAUTH1:
        h = app_headers(extra)
        h["authorization"] = oauth1_header(method, url, params)
        return h
    return web_headers(extra)


def rate_wait(r: requests.Response, cap: int = 900) -> int:
    try:
        wait = int(r.headers.get("x-rate-limit-reset", "")) - int(time.time()) + 1
    except (TypeError, ValueError):
        wait = 60
    return max(5, min(wait, cap))


def post_with_retry(url: str, tries: int = 3, **kwargs) -> requests.Response:
    last = None
    for _ in range(tries):
        last = requests.post(url, **kwargs)
        if last.status_code != 429:
            return last
        w = rate_wait(last)
        log(f"  ⏳ 429 — انتظار {w}s")
        time.sleep(w)
    return last


# ---------------- Session check ----------------
class SessionDeadError(RuntimeError):
    pass


class DailyLimitError(RuntimeError):
    pass


def check_session() -> dict:
    url = "https://api.x.com/2/badge_count/badge_count.json"
    params = {"supports_ntab_urt": "1", "include_xchat_count": "1"}
    r = requests.get(url, params=params, headers=auth_for("GET", url, params), timeout=30)
    if r.status_code in (401, 403):
        raise SessionDeadError(f"badge_count {r.status_code}: جلسة غير صالحة")
    if r.status_code != 200:
        raise RuntimeError(f"badge_count {r.status_code}: {r.text[:200]}")
    j = r.json()
    log(f"🔎 الجلسة حيّة — unread={j.get('total_unread_count', 0)} "
        f"(ntab={j.get('ntab_unread_count', 0)}, dm={j.get('dm_unread_count', 0)})")
    return j


def seconds_until_utc_midnight(pad: int = 180, jitter: int = 300) -> int:
    now = time.time()
    t = time.gmtime(now)
    secs_today = t.tm_hour * 3600 + t.tm_min * 60 + t.tm_sec
    wait = 86400 - secs_today + pad + random.randint(0, jitter)
    return max(600, int(wait))


# ---------------- Media ----------------
def _switch_upload_url() -> bool:
    if _upload_url[0] == UPLOAD_APP and not USE_OAUTH1:
        _upload_url[0] = UPLOAD_WEB
        log(f"  ↪️  تحويل الرفع إلى {UPLOAD_WEB}")
        return True
    return False


def upload_init(total: int, mime: str, category: str) -> str:
    data = {
        "command": "INIT",
        "total_bytes": str(total),
        "media_type": mime,
        "media_category": category,
    }
    if _upload_url[0] == UPLOAD_APP:
        data["enable_1080p_variant"] = "true"
        data["enable_4k_variant"] = "true"

    for attempt in (0, 1):
        url = _upload_url[0]
        r = post_with_retry(url, data=data, headers=auth_for("POST", url), timeout=60)
        if r.status_code in (200, 202):
            return r.json()["media_id_string"]
        if attempt == 0 and r.status_code in (400, 401, 403, 404, 410) and _switch_upload_url():
            continue
        raise RuntimeError(f"INIT {r.status_code}: {r.text[:300]}")
    raise RuntimeError("INIT: فشل المساران")


def upload_append(mid: str, chunk: bytes, mime: str, idx: int) -> None:
    url = _upload_url[0]
    params = {"command": "APPEND", "media_id": mid, "segment_index": str(idx)}
    boundary = str(uuid.uuid4())
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"\r\n'
        f"Content-Transfer-Encoding: binary\r\n"
        f"Content-Type: {mime}\r\n\r\n"
    ).encode() + chunk + f"\r\n--{boundary}--\r\n".encode()
    r = post_with_retry(
        url,
        params=params,
        data=body,
        headers=auth_for("POST", url, params,
                         {"content-type": f"multipart/form-data; boundary={boundary}"}),
        timeout=300,
    )
    if r.status_code not in (200, 202, 204):
        raise RuntimeError(f"APPEND {idx} {r.status_code}: {r.text[:300]}")


def upload_finalize(mid: str) -> dict:
    url = _upload_url[0]
    r = post_with_retry(
        url,
        data={"command": "FINALIZE", "media_id": mid},
        headers=auth_for("POST", url),
        timeout=60,
    )
    if r.status_code not in (200, 201):
        raise RuntimeError(f"FINALIZE {r.status_code}: {r.text[:300]}")
    return r.json()


def upload_status(mid: str) -> dict:
    url = _upload_url[0]
    params = {"command": "STATUS", "media_id": mid}
    r = requests.get(url, params=params, headers=auth_for("GET", url, params), timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"STATUS {r.status_code}: {r.text[:300]}")
    return r.json()


def wait_processing(mid: str, timeout: int = 900) -> None:
    start = time.time()
    while True:
        p = (upload_status(mid).get("processing_info") or {})
        state = p.get("state")
        if not state:
            return
        if state == "succeeded":
            log("    ✅ المعالجة اكتملت")
            return
        if state == "failed":
            raise RuntimeError(
                f"processing failed: {json.dumps(p.get('error') or {}, ensure_ascii=False)}"
            )
        w = int(p.get("check_after_secs") or 3)
        if time.time() - start > timeout:
            raise RuntimeError("processing timeout")
        log(f"    ⏳ {state} — {p.get('progress_percent', '?')}%")
        time.sleep(w)


def upload_media(data: bytes, mime: str, category: str) -> str:
    mid = upload_init(len(data), mime, category)
    n = max(1, (len(data) + CHUNK_VIDEO - 1) // CHUNK_VIDEO)
    for i in range(n):
        upload_append(mid, data[i * CHUNK_VIDEO:(i + 1) * CHUNK_VIDEO], mime, i)
        log(f"    ⬆️  chunk {i + 1}/{n}")
    fin = upload_finalize(mid)
    if (fin.get("processing_info") or {}).get("state"):
        wait_processing(mid)
    return mid


# ---------------- CreatePost ----------------
def _post_via_graphql(text: str, media_ids: list[str]) -> dict:
    variables = {
        "post_text": text, "reply": None,
        "media": {"media_entities": [{"media_id": m, "tagged_users": []} for m in media_ids]},
        "attachment_url": None, "exclusive_tweet_control_options": None,
        "semantic_core_ids": None, "conversation_control": None,
        "broadcast_to_followers": None, "card_uri": None,
        "cashtag_attachment_options": None, "edit_options": {}, "geo": None,
        "content_disclosure_options": None, "narrowcast_place_options": None,
        "reaction_context_options": None, "engagement_request": None,
    }
    body = {
        "variables": json.dumps(variables, separators=(",", ":"), ensure_ascii=False),
        "features": json.dumps(CREATE_FEATURES, separators=(",", ":")),
    }
    url = (f"https://api.x.com/graphql/{OP_CREATE_POST}/CreatePost" if USE_OAUTH1
           else f"https://x.com/i/api/graphql/{OP_CREATE_POST}/CreatePost")
    hdr = auth_for("POST", url, None,
                   {"Content-Type": "application/json", "Accept": "application/json"})
    r = post_with_retry(url, json=body, headers=hdr, timeout=60)
    try:
        return r.json()
    except ValueError:
        raise RuntimeError(f"CreatePost رد غير JSON: {r.status_code} {r.text[:300]}")


def _post_via_v11(text: str, media_ids: list[str]) -> dict:
    if not USE_OAUTH1:
        raise RuntimeError("v1.1 يتطلب OAuth1 (X_TOKEN_SECRET)")
    url = "https://upload.x.com/1.1/statuses/update.json"
    form = {"status": text, "media_ids": ",".join(media_ids)}
    hdr = auth_for("POST", url, form, {"Content-Type": "application/x-www-form-urlencoded"})
    r = post_with_retry(url, data=form, headers=hdr, timeout=60)
    try:
        j = r.json()
    except ValueError:
        raise RuntimeError(f"statuses/update رد غير JSON: {r.status_code} {r.text[:200]}")
    if j.get("id_str"):
        return {"data": {"create_tweet": {"tweet_results": {"result": {
            "rest_id": j["id_str"],
            "core": {"user_results": {"result": {"core": {"screen_name": SCREEN_NAME}}}},
        }}}}}
    raise RuntimeError(f"statuses/update {r.status_code}: {json.dumps(j, ensure_ascii=False)[:300]}")


def create_post(text: str, media_ids: list[str]) -> dict:
    j = _post_via_graphql(text, media_ids)
    if (j.get("data") or {}).get("create_tweet"):
        return j

    errs = j.get("errors") or []
    code = errs[0].get("code") if errs else None
    msg = (errs[0].get("message") if errs else "") or json.dumps(j, ensure_ascii=False)[:300]
    low = msg.lower()

    if code in (32, 89) or "could not authenticate" in low or "invalid or expired token" in low:
        raise SessionDeadError(msg)
    if code == 344 or "daily limit" in low:
        raise DailyLimitError(msg)

    if USE_OAUTH1 and (code in (38, 404) or "query" in low or "unknown" in low):
        log("  ↪️  GraphQL رفض — محاولة v1.1 statuses/update")
        return _post_via_v11(text, media_ids)

    raise RuntimeError(f"CreatePost ({code}): {msg}")


# ---------------- Caption ----------------
def hashtag(tag: str) -> str:
    t = tag.strip().lower().replace("-", "_").replace(" ", "_")
    return "#" + t if t else ""


def build_caption(video: dict) -> str:
    title = (video.get("title") or "").strip()
    chars = [c.get("name", "").strip()
             for c in (video.get("characters") or []) if c.get("name")]
    cats = video.get("categories") or list((video.get("tags") or {}).keys())
    tags = " ".join(h for h in (hashtag(c) for c in cats) if h)
    parts = [title]
    if chars:
        parts += ["", ", ".join(chars)]
    if tags:
        parts += ["", "", tags]
    return "\n".join(parts).strip()


# ---------------- Download ----------------
def download(url: str) -> bytes:
    r = requests.get(url, headers={"User-Agent": WEB_UA}, timeout=300, stream=True)
    if r.status_code != 200:
        raise RuntimeError(f"تنزيل {r.status_code}")
    buf = bytearray()
    for chunk in r.iter_content(1024 * 128):
        if chunk:
            buf.extend(chunk)
    return bytes(buf)


# ---------------- State ----------------
def load_db() -> list[dict]:
    if not DB_FILE.exists():
        raise SystemExit(f"✖ {DB_FILE} غير موجود.")
    data = json.loads(DB_FILE.read_text(encoding="utf-8"))
    videos = data.get("videos") if isinstance(data, dict) else data
    if not isinstance(videos, list):
        raise SystemExit("✖ حقل videos مفقود.")
    return videos


def load_posted() -> set[str]:
    if not POSTED_FILE.exists():
        return set()
    try:
        d = json.loads(POSTED_FILE.read_text(encoding="utf-8"))
        return set(str(x) for x in d.get("ids", []))
    except Exception:
        return set()


def save_posted(ids: set[str]) -> None:
    POSTED_FILE.write_text(
        json.dumps({"ids": sorted(ids), "updated": time.strftime("%Y-%m-%dT%H:%M:%S")},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def save_state(video: dict, caption: str, media_id: str) -> None:
    STATE_FILE.write_text(json.dumps({
        "id": video.get("id"), "title": video.get("title"),
        "caption": caption, "media_id": media_id,
        "saved_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }, ensure_ascii=False, indent=2), encoding="utf-8")


def load_state() -> dict | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def clear_state() -> None:
    try:
        STATE_FILE.unlink()
    except FileNotFoundError:
        pass


# ---------------- Publish one ----------------
def publish_video(video: dict) -> bool:
    vid = str(video.get("id") or "?")
    title = video.get("title") or ""
    caption = build_caption(video)
    log(f"🎬 [{vid}] {title}")
    log("── الوصف ──")
    for line in caption.split("\n"):
        log("   " + line)
    log("────────────")

    mp4 =video.get("mp4")
    if not mp4:
        log("  ⚠️  بدون mp4 — تخطّي.")
        return False

    log("⬇️  تنزيل ...")
    data = download(mp4)
    size_mb = len(data) / (1024 * 1024)
    log(f"📦 {size_mb:.2f} MB")
    if size_mb > 512:
        log("  ⚠️  > 512MB — تخطّي.")
        return False

    mime = mimetypes.guess_type(mp4)[0] or "video/mp4"
    if not mime.startswith("video/"):
        mime = "video/mp4"

    log(f"1/2 رفع الفيديو ({MEDIA_CATEGORY}) ...")
    mid = upload_media(data, mime, MEDIA_CATEGORY)
    save_state(video, caption, mid)
    log(f"    💾 media_id={mid}")

    log("2/2 إنشاء المنشور ...")
    result = create_post(caption, [mid])
    try:
        tw = result["data"]["create_tweet"]["tweet_results"]["result"]
        rid = tw.get("rest_id") or ""
        sn = ((tw.get("core") or {}).get("user_results") or {}) \
            .get("result", {}).get("core", {}).get("screen_name", "")
    except (KeyError, TypeError):
        rid, sn = "", ""

    if rid:
        log(f"✅ نُشر: https://x.com/{sn or SCREEN_NAME}/status/{rid}")
        clear_state()
        return True

    log("⚠️  استجابة غير مفهومة — media_id محفوظ.")
    return False


# ---------------- Retry helper ----------------
def retry_pending() -> bool:
    st = load_state()
    if not st or not st.get("media_id"):
        return False
    log(f"♻️  محاولة نشر معلّق: [{st.get('id')}] {st.get('title')} — media_id={st['media_id']}")
    result = create_post(st["caption"], [st["media_id"]])
    try:
        rid = result["data"]["create_tweet"]["tweet_results"]["result"].get("rest_id")
    except (KeyError, TypeError):
        rid = ""
    if rid:
        log(f"✅ تم نشر المعلّق — id={rid}")
        if st.get("id"):
            ids = load_posted()
            ids.add(str(st["id"]))
            save_posted(ids)
        clear_state()
        return True
    return False


# ---------------- Auto loop ----------------
def pick_next(videos: list[dict], posted: set[str]) -> dict | None:
    remaining = [v for v in videos if str(v.get("id")) not in posted and v.get("mp4")]
    if not remaining:
        return None
    random.shuffle(remaining)
    return remaining[0]


def sleep_with_log(seconds: int, reason: str = "") -> None:
    if seconds <= 0:
        return
    if reason:
        log(f"💤 {reason} — نوم {seconds // 3600}h{(seconds % 3600) // 60}m")
    target = time.time() + seconds
    while True:
        left = int(target - time.time())
        if left <= 0:
            return
        time.sleep(min(left, 600))


def run_loop(min_hours: float = 3.0, max_hours: float = 4.0, once: bool = False) -> None:
    log("=" * 50)
    log(f"🤖 AutoPoster — @{SCREEN_NAME}  (auth={'OAuth1' if USE_OAUTH1 else 'Bearer'})")
    log(f"   فاصل: {min_hours}h–{max_hours}h  |  رفع: {_upload_url[0]}")
    log("=" * 50)

    try:
        check_session()
    except SessionDeadError as exc:
        log(f"🔑 {exc} — أوقف.")
        return
    except Exception as exc:
        log(f"⚠️  فحص الجلسة: {exc} — أكمل على أي حال.")

    videos = load_db()
    log(f"📚 القاعدة: {len(videos)} فيديو")

    while True:
        posted = load_posted()
        log(f"📌 المنشور سابقاً: {len(posted)} / {len(videos)}")

        if len(posted) >= len(videos):
            log("🎉 انتهت كل الفيديوهات في القاعدة.")
            return

        try:
            if retry_pending():
                if once:
                    return
                sleep_with_log(int(random.uniform(min_hours, max_hours) * 3600), "الدورة التالية")
                continue
        except DailyLimitError as exc:
            if once:
                log(f"🚫 {exc} — وضع once، أتوقف.")
                return
            wait = seconds_until_utc_midnight()
            log(f"🚫 {exc} — حد يومي؛ ننتظر تجدّد الحد (منتصف ليل UTC).")
            sleep_with_log(wait, "تجدّد الحد اليومي")
            continue
        except SessionDeadError as exc:
            log(f"🔑 الجلسة ميتة — أوقف: {exc}")
            return

        video = pick_next(videos, posted)
        if not video:
            log("لا مرشّح للنشر — أتوقف.")
            return

        try:
            ok = publish_video(video)
        except DailyLimitError as exc:
            if once:
                log(f"🚫 {exc} — وضع once، أتوقف. media_id محفوظ للنشر لاحقاً.")
                return
            wait = seconds_until_utc_midnight()
            log(f"🚫 {exc} — حد يومي؛ media_id محفوظ، ننتظر {wait // 3600}h{(wait % 3600) // 60}m.")
            sleep_with_log(wait, "تجدّد الحد اليومي")
            continue
        except SessionDeadError as exc:
            log(f"🔑 {exc} — أوقف.")
            return
        except Exception as exc:
            log(f"❌ فشل [{video.get('id')}]: {exc}")
            posted.add(str(video.get("id")))
            save_posted(posted)
            ok = False

        if ok:
            ids = load_posted()
            ids.add(str(video.get("id")))
            save_posted(ids)

        if once:
            return

        sleep_with_log(int(random.uniform(min_hours, max_hours) * 3600), "الدورة التالية")


# ---------------- Entry ----------------
def main() -> int:
    if "--check" in sys.argv:
        try:
            check_session()
        except SessionDeadError as exc:
            log(f"🔑 {exc}")
            return 2
        except Exception as exc:
            log(f"⚠️  {exc}")
            return 1
        return 0

    min_h = float(os.environ.get("MIN_HOURS", "3"))
    max_h = float(os.environ.get("MAX_HOURS", "4"))
    once = "--once" in sys.argv
    try:
        run_loop(min_h, max_h, once=once)
    except KeyboardInterrupt:
        log("⏹ أُلغي يدوياً.")
        return 130
    return 0


if __name__ == "__main__":
    sys.exit(main())
