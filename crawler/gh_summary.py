from __future__ import annotations

import json
import sys
from pathlib import Path


def _print_per_source_stats(stats: dict) -> None:
    if not stats:
        print("\nNo per-source stats recorded.")
        return

    print("\nPer-source stats:")
    print(
        "| Source | Fetched | New | Skipped | Status | Failure Streak | Zero New Streak | Last Run |"
    )
    print("| --- | ---: | ---: | ---: | --- | ---: | ---: | --- |")

    for source_id in sorted(stats):
        info = stats.get(source_id) or {}
        print(
            "| {source} | {fetched} | {new} | {skipped} | {status} | {failure} | {zero_new} | {last_run} |".format(
                source=source_id,
                fetched=info.get("fetched", 0),
                new=info.get("new", 0),
                skipped=info.get("skipped", 0),
                status=info.get("status", ""),
                failure=info.get("failure_streak", 0),
                zero_new=info.get("zero_new_streak", 0),
                last_run=info.get("last_run", ""),
            )
        )


def _print_alerts(alerts: list[dict]) -> None:
    if not alerts:
        return

    print("\nAlerts:")
    for alert in alerts:
        print(
            "- {source}: {alert_type} (streak={streak}) {message} last_run={last_run} last_error={last_error}".format(
                source=alert.get("source_id"),
                alert_type=alert.get("type"),
                streak=alert.get("streak"),
                message=alert.get("message", ""),
                last_run=alert.get("last_run", ""),
                last_error=alert.get("last_error", ""),
            )
        )


def main(argv: list[str]) -> int:
    index_path = Path(argv[1]) if len(argv) > 1 else Path("data/index.json")
    if not index_path.exists():
        print("\nNo index.json available for per-source stats.")
        return 0

    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("\nindex.json is not valid JSON.")
        return 0

    stats = payload.get("last_run", {}).get("sources", {}) or {}
    _print_per_source_stats(stats)

    alerts = payload.get("alerts", []) or []
    _print_alerts(alerts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
