#!/usr/bin/env python3
"""Hit the live app so Prometheus/Grafana request graphs move.

Load  = expected traffic (default).
Stress = more workers, same endpoints, watch latency rise.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import time
import urllib.error
import urllib.request

PATHS = ("/health", "/version", "/environment", "/ready")


def hit(base: str, path: str) -> int:
    url = base.rstrip("/") + path
    try:
        with urllib.request.urlopen(url, timeout=5) as res:
            return int(res.status)
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate traffic for Grafana graphs")
    parser.add_argument("--url", default="http://127.0.0.1:5000")
    parser.add_argument("--seconds", type=int, default=45)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--stress",
        action="store_true",
        help="higher concurrency so latency graphs move",
    )
    args = parser.parse_args()
    if args.stress:
        args.workers = max(args.workers, 32)
        if args.seconds < 60:
            args.seconds = 60

    mode = "stress" if args.stress else "load"
    print(f"{mode} test  {args.url}  workers={args.workers}  {args.seconds}s")
    print("leave Grafana open on Request rate and Requests by status")

    ok = fail = 0
    deadline = time.time() + args.seconds
    started = time.time()

    def one(_n: int) -> int:
        path = PATHS[_n % len(PATHS)]
        return hit(args.url, path)

    n = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        while time.time() < deadline:
            batch = args.workers * 4
            results = list(pool.map(one, range(n, n + batch)))
            n += batch
            for status in results:
                if 200 <= status < 400:
                    ok += 1
                else:
                    fail += 1

    elapsed = max(time.time() - started, 0.001)
    print(f"ok={ok}  fail={fail}  rps={ok / elapsed:.1f}")
    print("wait ~15s then look at Grafana Request rate")


if __name__ == "__main__":
    main()
