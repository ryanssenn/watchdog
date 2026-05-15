## vLLM Benchmarking

This project provides a practical benchmarking framework for measuring performance behavior of the vLLM inference engine.

It is designed for vLLM maintainers who need to compare performance across configurations and, eventually, detect regressions across releases under controlled workloads.

The goal is to run controlled workloads, vary one configuration at a time, and measure how latency and throughput change. This makes performance differences observable and comparable across runs.

This is not an automated regression detection system. The current focus is benchmarking and configuration comparison. Regression detection is a roadmap item.

---

## Quick start (regression pipeline)

Run these commands from the **project root** (the directory that contains `make_two_jsons.py` and the `results/` folder — not inside `results/`).

Requires Python 3 and `results/qwen_bench.json` (GuideLLM benchmark output).

### macOS / Linux

```bash
cd /path/to/watchdog

python3 ./make_two_jsons.py ./results/qwen_bench.json ./results/fp16/chat.json ./results/fp8/chat.json regress
python3 ./extract_metrics.py ./results/fp16/chat.json ./results/fp16/chat.metrics.json
python3 ./extract_metrics.py ./results/fp8/chat.json ./results/fp8/chat.metrics.json
python3 ./check_regressions.py ./results/fp16/chat.metrics.json ./results/fp8/chat.metrics.json
```

Use `python` instead of `python3` if that is what your environment provides.

On macOS/Linux, use forward slashes (`./results/...`). Backslashes (`.\results\...`) are Windows-style and will not work correctly in zsh or bash.

### Windows (PowerShell)

```powershell
cd C:\path\to\watchdog

python .\make_two_jsons.py .\results\qwen_bench.json .\results\fp16\chat.json .\results\fp8\chat.json regress
python .\extract_metrics.py .\results\fp16\chat.json .\results\fp16\chat.metrics.json
python .\extract_metrics.py .\results\fp8\chat.json .\results\fp8\chat.metrics.json
python .\check_regressions.py .\results\fp16\chat.metrics.json .\results\fp8\chat.metrics.json
```

Use your Python install (for example `py -3` or a full path to `python.exe`) if `python` is not on your PATH.

### What the steps do

1. **`make_two_jsons.py`** — Builds `fp16/chat.json` (baseline) and `fp8/chat.json` from `qwen_bench.json`. With `regress`, the FP8 file is intentionally 10% worse for demo/testing.
2. **`extract_metrics.py`** — Extracts TTFT p99, output tokens/sec, and requests/sec into `.metrics.json` files.
3. **`check_regressions.py`** — Compares base vs test metrics; prints `REGRESSION` or `OK` and exits with code 1 if any metric regressed.

Expected output with `regress` mode: +10% TTFT, −10% throughput on all three metrics.

---

## Benchmark Roadmap (Compounding Optimizations)

Benchmarks are being structured as a stack of incremental optimizations on the same model, hardware, and workload:

- FP16 baseline  
- FP8 quantization  
- FP8 + speculative decoding  
- TurboQuant  

Each step builds on the previous one. The goal is to measure the delta introduced by each optimization, not evaluate configurations in isolation.

---

## Metrics

Each run captures:

- Time to First Token (TTFT)  
- Tokens per second (TPS)  
- Requests per second  

These metrics describe latency, decoding efficiency, and throughput.

---

## Roadmap

- Commit reproducible benchmark scenarios (YAML + workload definitions)  
- Document hardware setup used for all runs  
- Establish FP16 baseline on fixed model and workload  
- Re-run FP8 under identical conditions  
- Add side-by-side comparison table (TTFT, TPS, req/s at matched concurrency)  
- Write short results analysis explaining observed deltas  

- Add FP8 + speculative decoding
- Extend comparison to full optimization stack (FP16 → FP8 → FP8 + spec → TurboQuant if available)  

- Add automated comparison (compute % deltas between runs)  
- Define regression thresholds (e.g. TTFT +10%, TPS -5%)  
- Flag regressions in output  

- Integrate into CI for release benchmarking  
