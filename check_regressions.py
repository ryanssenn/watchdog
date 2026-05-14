import json
import sys

# Usage:
#   python check_regressions.py <base_metrics.json> <test_metrics.json>

if len(sys.argv) < 3:
    raise SystemExit(
        "Usage: python check_regressions.py <base_metrics.json> <test_metrics.json>"
    )

BASE = sys.argv[1]
TEST = sys.argv[2]


def load_metrics(path):
    """
    Accepts any of:
      { "metrics": {...} }
      { "summary": {...} }
      { "ttft_p99_ms": ..., ... }
    Returns a flat dict of metrics.
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        if "metrics" in data and isinstance(data["metrics"], dict):
            return data["metrics"]
        if "summary" in data and isinstance(data["summary"], dict):
            return data["summary"]
        return data

    raise SystemExit(f"Invalid JSON structure in {path}")


base = load_metrics(BASE)
test = load_metrics(TEST)

required = [
    "ttft_p99_ms",
    "output_tokens_per_second",
    "requests_per_second",
]

missing = [k for k in required if k not in base or k not in test]
if missing:
    raise SystemExit(
        "Missing expected metrics.\n"
        f"Missing keys: {missing}\n"
        f"Base keys: {list(base.keys())}\n"
        f"Test keys: {list(test.keys())}"
    )

print("Regression report:\n")


def pct_change(base_v, test_v):
    base_v = float(base_v)
    test_v = float(test_v)
    if base_v == 0.0:
        return float("inf")
    return (test_v - base_v) / base_v * 100.0


EXIT_CODE = 0

for key in required:
    b = float(base[key])
    t = float(test[key])
    delta = pct_change(b, t)

    # Interpretation rules:
    # - For latency (ttft): higher is worse
    # - For throughput: lower is worse
    if key == "ttft_p99_ms":
        regressed = delta > 0
    else:
        regressed = delta < 0

    status = "REGRESSION" if regressed else "OK"
    sign = "+" if delta >= 0 else ""

    print(
        f"{key:28} "
        f"base={b:.4f}  test={t:.4f}  "
        f"change={sign}{delta:.2f}%  "
        f"{status}"
    )

    if regressed:
        EXIT_CODE = 1

sys.exit(EXIT_CODE)