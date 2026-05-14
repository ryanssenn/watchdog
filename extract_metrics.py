import json
import sys

# Usage:
#   python extract_metrics.py <guidellm_results.json> <metrics_out.json>
#
# Output format:
# {
#   "metrics": {
#     "ttft_p99_ms": <float>,
#     "output_tokens_per_second": <float>,
#     "requests_per_second": <float>
#   }
# }

if len(sys.argv) < 3:
    raise SystemExit("Usage: python extract_metrics.py <guidellm_results.json> <metrics_out.json>")

inp = sys.argv[1]
out = sys.argv[2]

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


def extract_from_old_summary(d):
    """
    Old/simple format:
      {
        "summary": {
          "time_to_first_token": {"p99": ...},
          "output_tokens_per_second": {"mean": ...},
          "requests_per_second": {"mean": ...}
        }
      }
    or those keys at the top-level.
    """
    s = d.get("summary", d)
    ttft = pick_first(s, [["time_to_first_token", "p99"]])
    tps = pick_first(s, [["output_tokens_per_second", "mean"]])
    rps = pick_first(s, [["requests_per_second", "mean"]])

    if ttft is None or tps is None or rps is None:
        return None
    return float(ttft), float(tps), float(rps)


def extract_from_guidellm_report(d):
    """
    GuideLLM report format usually contains:
      { "benchmarks": [ { "metrics": {...} }, ... ] }

    The GuideLLM docs show metrics accessed per-benchmark, e.g.:
      benchmark.metrics.requests_per_second.successful.mean
      benchmark.metrics.time_to_first_token_ms.successful.percentiles.p99
      """
    bms = d.get("benchmarks")
    if not isinstance(bms, list) or not bms:
        return None

    rps_paths = [
        ["metrics", "requests_per_second", "successful", "mean"],
        ["metrics", "requests_per_second", "mean"],
    ]
    ttft_paths = [
        ["metrics", "time_to_first_token_ms", "successful", "percentiles", "p99"],
        ["metrics", "time_to_first_token_ms", "percentiles", "p99"],
        ["metrics", "time_to_first_token_ms", "successful", "p99"],
    ]
    tps_paths = [
        ["metrics", "output_tokens_per_second", "successful", "mean"],
        ["metrics", "output_tokens_per_second", "mean"],
        ["metrics", "tokens_per_second", "successful", "mean"],
        ["metrics", "tokens_per_second", "mean"],
    ]

    # We'll pick the benchmark entry with the highest RPS
    best = None  # (rps, ttft_ms, tps)

    for b in bms:
        rps = pick_first(b, rps_paths)
        ttft = pick_first(b, ttft_paths)
        tps = pick_first(b, tps_paths)

        if rps is None or ttft is None or tps is None:
            continue

        triple = (float(rps), float(ttft), float(tps))

        if best is None or triple[0] > best[0]:
            best = triple

    if best is None:
        return None

    rps, ttft_ms, tps = best
    # Return (ttft_p99_ms, output_tokens_per_second_mean, requests_per_second_mean)
    return ttft_ms, tps, rps


triple = extract_from_old_summary(data) or extract_from_guidellm_report(data)

if triple is None:
    top_keys = list(data.keys()) if isinstance(data, dict) else type(data).__name__
    raise SystemExit(
        "Could not find metrics.\n"
        "Expected either:\n"
        "  - summary.time_to_first_token.p99, summary.output_tokens_per_second.mean, summary.requests_per_second.mean\n"
        "or a GuideLLM report with benchmarks[*].metrics.*.\n"
        f"Top-level keys in this JSON: {top_keys}\n"
    )

ttft_ms, tps, rps = triple

metrics = {
    "metrics": {
        "ttft_p99_ms": float(ttft_ms),
        "output_tokens_per_second": float(tps),
        "requests_per_second": float(rps),
    }
}

with open(out, "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print("Wrote", out)