## vLLM Benchmarking

This project provides a practical benchmarking framework for measuring performance behavior of the vLLM inference engine.

It is designed for vLLM maintainers who need to compare performance across configurations and, eventually, detect regressions across releases under controlled workloads.

The goal is to run controlled workloads, vary one configuration at a time, and measure how latency and throughput change. This makes performance differences observable and comparable across runs.

This is not an automated regression detection system. The current focus is benchmarking and configuration comparison. Regression detection is a roadmap item.

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
