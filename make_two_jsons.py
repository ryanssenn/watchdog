import json
import sys

# Usage:
#   python make_two_jsons.py <input.json> <base_out.json> <test_out.json> [nochange|regress|improve]

if len(sys.argv) < 5:
    raise SystemExit("Usage: python make_two_jsons.py <input.json> <base_out.json> <test_out.json> [nochange|regress|improve]")

inp = sys.argv[1]
base_out = sys.argv[2]
test_out = sys.argv[3]
mode = sys.argv[4].strip().lower()

with open(inp, "r", encoding="utf-8") as f:
    data = json.load(f)


def get_path(obj, path):
    cur = obj
    for p in path:
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def pick_first(obj, candidates):
    for path in candidates:
        v = get_path(obj, path)
        if v is not None:
            return v
    return None


def extract_three(d):
    """
    Returns: (ttft_p99_ms, output_tokens_per_second_mean, requests_per_second_mean)
    Supports:
      - old simple summary format
      - GuideLLM benchmarks report format [1](https://outlook.live.com/calendar/item/AQMkADAwATM0MDAAMi05MWFjLWFmZTYtMDACLTAwCgFRAAgIAN63lRE2wABGAAACkakKay1wkE6LoKoHZksnTAcA9r9wZP5-CkCeejaZu5Ma_QAAAgENAAAA9r9wZP5-CkCeejaZu5Ma_QAAAJoBu4AAAAAQ)
    """

    # --- Old/simple format ---
    s = d.get("summary", d)
    ttft = pick_first(s, [["time_to_first_token", "p99"]])
    tps = pick_first(s, [["output_tokens_per_second", "mean"]])
    rps = pick_first(s, [["requests_per_second", "mean"]])
    if ttft is not None and tps is not None and rps is not None:
        return float(ttft), float(tps), float(rps)

    # --- GuideLLM report format ---
    bms = d.get("benchmarks")
    if isinstance(bms, list) and bms:
        rps_paths = [
            ["metrics", "requests_per_second", "successful", "mean"],
            ["metrics", "requests_per_second", "mean"],
        ]
        ttft_paths = [
            ["metrics", "time_to_first_token_ms", "successful", "percentiles", "p99"],
            ["metrics", "time_to_first_token_ms", "percentiles", "p99"],
        ]
        tps_paths = [
            ["metrics", "output_tokens_per_second", "successful", "mean"],
            ["metrics", "output_tokens_per_second", "mean"],
            ["metrics", "tokens_per_second", "successful", "mean"],
            ["metrics", "tokens_per_second", "mean"],
        ]

        best = None  # (rps, ttft_ms, tps)
        for b in bms:
            rps_v = pick_first(b, rps_paths)
            ttft_v = pick_first(b, ttft_paths)
            tps_v = pick_first(b, tps_paths)

            if rps_v is None or ttft_v is None or tps_v is None:
                continue

            triple = (float(rps_v), float(ttft_v), float(tps_v))

            if best is None or triple[0] > best[0]:
                best = triple

        if best is not None:
            rps_best, ttft_ms_best, tps_best = best
            return float(ttft_ms_best), float(tps_best), float(rps_best)

    return None


triple = extract_three(data)
if triple is None:
    top_keys = list(data.keys()) if isinstance(data, dict) else type(data).__name__
    raise SystemExit(
        "Could not find metrics. Expected either:\n"
        "  - data['summary'] with time_to_first_token.p99, output_tokens_per_second.mean, requests_per_second.mean\n"
        "or:\n"
        "  - a GuideLLM report with data['benchmarks'][*]['metrics'] containing TTFT p99 + throughput.\n"
        f"Top-level keys in this JSON: {top_keys}"
    )

ttft_ms, tps, rps = triple


def emit_summary(ttft_ms_val, tps_val, rps_val):
    return {
        "summary": {
            "time_to_first_token": {"p99": float(ttft_ms_val)},
            "output_tokens_per_second": {"mean": float(tps_val)},
            "requests_per_second": {"mean": float(rps_val)},
        }
    }


base_json = emit_summary(ttft_ms, tps, rps)

if mode == "nochange":
    test_json = emit_summary(ttft_ms, tps, rps)

elif mode == "regress":
    # Worse: TTFT up, throughput down
    test_json = emit_summary(ttft_ms * 1.10, tps * 0.90, rps * 0.90)

elif mode == "improve":
    # Better: TTFT down, throughput up
    test_json = emit_summary(ttft_ms * 0.90, tps * 1.10, rps * 1.10)

else:
    raise SystemExit("Mode must be one of: nochange, regress, improve")


with open(base_out, "w", encoding="utf-8") as f:
    json.dump(base_json, f, indent=2)

with open(test_out, "w", encoding="utf-8") as f:
    json.dump(test_json, f, indent=2)

print("Wrote", base_out, "and", test_out)