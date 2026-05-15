Run the regression pipeline from the project root (parent of this folder).
See ../README.md#quick-start-regression-pipeline for full macOS/Linux and Windows commands.

macOS / Linux (from watchdog/):

  python3 ./make_two_jsons.py ./results/qwen_bench.json ./results/fp16/chat.json ./results/fp8/chat.json regress
  python3 ./extract_metrics.py ./results/fp16/chat.json ./results/fp16/chat.metrics.json
  python3 ./extract_metrics.py ./results/fp8/chat.json ./results/fp8/chat.metrics.json
  python3 ./check_regressions.py ./results/fp16/chat.metrics.json ./results/fp8/chat.metrics.json

Windows (PowerShell, from watchdog\):

  python .\make_two_jsons.py .\results\qwen_bench.json .\results\fp16\chat.json .\results\fp8\chat.json regress
  python .\extract_metrics.py .\results\fp16\chat.json .\results\fp16\chat.metrics.json
  python .\extract_metrics.py .\results\fp8\chat.json .\results\fp8\chat.metrics.json
  python .\check_regressions.py .\results\fp16\chat.metrics.json .\results\fp8\chat.metrics.json
