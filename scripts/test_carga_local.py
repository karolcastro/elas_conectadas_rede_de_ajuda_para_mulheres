"""Run a synthetic in-process concurrency test against the local ASGI app.

This measures application/route behavior only. It does not measure hosting,
internet latency, a real network socket, external APIs, or monthly capacity.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import time
from collections.abc import Sequence

import httpx

from elas_conectadas_mcp.http_app import app


def percentile(values: list[float], percent: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((percent / 100) * len(ordered) + 0.5) - 1))
    return ordered[index]


async def run_scenario(request_count: int, concurrency: int) -> dict[str, int | float]:
    latencies: list[float] = []
    errors = 0
    semaphore = asyncio.Semaphore(concurrency)
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://localhost:8000",
        headers={"host": "localhost:8000"},
        timeout=10.0,
    ) as client:

        async def request_health() -> None:
            nonlocal errors
            async with semaphore:
                started = time.perf_counter()
                try:
                    response = await client.get("/health")
                    elapsed = (time.perf_counter() - started) * 1000
                    latencies.append(elapsed)
                    if response.status_code != 200 or response.json().get("status") != "ok":
                        errors += 1
                except (httpx.HTTPError, ValueError):
                    errors += 1
                    latencies.append((time.perf_counter() - started) * 1000)

        started_all = time.perf_counter()
        await asyncio.gather(*(request_health() for _ in range(request_count)))
        duration = time.perf_counter() - started_all

    return {
        "requests": request_count,
        "concurrency": concurrency,
        "errors": errors,
        "duration_seconds": round(duration, 4),
        "requests_per_second": round(request_count / duration, 2) if duration else 0.0,
        "latency_ms_avg": round(statistics.mean(latencies), 2) if latencies else 0.0,
        "latency_ms_p50": round(percentile(latencies, 50), 2),
        "latency_ms_p95": round(percentile(latencies, 95), 2),
        "latency_ms_max": round(max(latencies), 2) if latencies else 0.0,
    }


async def main(request_count: int, concurrency_levels: Sequence[int]) -> int:
    results = []
    for concurrency in concurrency_levels:
        result = await run_scenario(request_count, concurrency)
        results.append(result)

    print(json.dumps(
        {
            "test": "local_asgi_health_check",
            "note": (
                "In-process synthetic test; not a hosting, internet, external API, "
                "or monthly-capacity benchmark."
            ),
            "results": results,
        },
        ensure_ascii=False,
        indent=2,
    ))
    return 1 if any(result["errors"] for result in results) else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requests", type=int, default=100, help="Requests per concurrency level.")
    parser.add_argument(
        "--concurrency",
        type=int,
        nargs="+",
        default=[1, 5, 10, 25, 50],
        help="Concurrency levels to test.",
    )
    args = parser.parse_args()
    if args.requests < 1 or any(level < 1 for level in args.concurrency):
        parser.error("requests and concurrency levels must be positive integers")
    raise SystemExit(asyncio.run(main(args.requests, args.concurrency)))
