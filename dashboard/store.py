import time
from collections import deque
from threading import Lock

_started = time.time()
_lock = Lock()
_ok = 0
_fail = 0
_events = deque(maxlen=40)


def uptime_seconds():
    return int(time.time() - _started)


def record(path, ok, status, ms):
    global _ok, _fail
    with _lock:
        if ok:
            _ok += 1
        else:
            _fail += 1
        _events.appendleft(
            {
                "ts": time.strftime("%H:%M:%S"),
                "path": path,
                "ok": bool(ok),
                "status": status,
                "ms": round(ms, 1),
            }
        )


def slo_snapshot(target):
    with _lock:
        total = _ok + _fail
        avail = 100.0 if total == 0 else (100.0 * _ok / total)
        error_pct = 0.0 if total == 0 else (100.0 * _fail / total)
        budget_pct = max(0.0, 100.0 - float(target))
        if budget_pct == 0:
            remaining = 100.0
        else:
            remaining = max(0.0, (budget_pct - error_pct) / budget_pct * 100.0)
        return {
            "target": float(target),
            "availability_pct": round(avail, 2),
            "error_pct": round(error_pct, 2),
            "error_budget_pct": round(budget_pct, 2),
            "budget_remaining_pct": round(remaining, 1),
            "good": _ok,
            "bad": _fail,
            "total": total,
        }


def recent_events():
    with _lock:
        return list(_events)
