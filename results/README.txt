... .\results\fp8\chat.metrics.json& c:\python314\python.exe ...

... .\results\fp16\chat.metrics.json& c:\python314\python.exe ...


USE IN TERMINAL:
& c:\python314\python.exe .\make_two_jsons.py .\results\qwen_bench.json .\results\fp16\chat.json .\results\fp8\chat.json regress
& c:\python314\python.exe .\extract_metrics.py .\results\fp16\chat.json .\results\fp16\chat.metrics.json
& c:\python314\python.exe .\extract_metrics.py .\results\fp8\chat.json  .\results\fp8\chat.metrics.json
& c:\python314\python.exe .\check_regressions.py .\results\fp16\chat.metrics.json .\results\fp8\chat.metrics.json