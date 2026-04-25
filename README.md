---

# Watchdog

Write README.md (20–25 min),
Paste this and adjust numbers:
vLLM Performance Regression Detection Framework,
This project demonstrates a reproducible benchmarking and observability pipeline
that detects latency and throughput regressions in vLLM inference deployments.

Motivation,
Performance regressions are silent failures in production LLM systems.
They increase cost, reduce throughput, and degrade user experience without
triggering functional errors.

Approach,
Benchmark vLLM using GuideLLM under a controlled workload,
Export key metrics (TTFT, TPS) via Prometheus,
Detect regressions using threshold-based comparison,
Validate remediation through configuration tuning,

Results,
Introduced a controlled batching regression,
Detected a 20%+ TTFT degradation,
Restored baseline performance through tuning,

Future Work,
CI/CD integration,
Cross-version vLLM regression testing,
Automated root-cause analysis,
Clear > clever

---
