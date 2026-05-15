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

ONE SHOT TEST FOR ALL REGRESSIONS:

& c:\python314\python.exe .\make_two_jsons.py `
  .\results\qwen_bench.json `
  .\results\fp16\chat.json `
  .\results\fp8\chat.json `
  regress

& c:\python314\python.exe .\extract_metrics.py .\results\fp16\chat.json .\results\fp16\chat.metrics.json
& c:\python314\python.exe .\extract_metrics.py .\results\fp8\chat.json  .\results\fp8\chat.metrics.json
& c:\python314\python.exe .\check_regressions.py .\results\fp16\chat.metrics.json .\results\fp8\chat.metrics.json

CHECK TO SEE IF PASS OR NOT / USE IN TERMINAL:

& c:\python314\python.exe .\check_regressions.py .\fp16_base_chat_c16.json .\fp8_base_chat_c16.json

$python = "c:\python314\python.exe"
& $python .\check_regressions.py .\fp16_base_chat_c16.json .\fp8_base_chat_c16.json
"Exit code was: $LASTEXITCODE"

CHECK TO SEE IF PASS OR NOT / USE IN TERMINAL:

$python = "c:\python314\python.exe"

& $python .\check_regressions.py .\fp16_base_chat_c16.json .\fp8_base_chat_c16.json
$code = $LASTEXITCODE   # capture immediately

switch ($code) {
  0 { Write-Host "PASSED (no regressions)"; exit 0 }
  1 { Write-Host "FAILED (regression detected)"; exit 1 }
  2 { Write-Host "ERROR (missing args / usage)"; exit 2 }
  default { Write-Host "ERROR (unexpected exit code=$code)"; exit $code }
}

Quick tip: prefer scripts for exit:
If you want to use exit codes (for CI or gating), put the logic into a file like run_check.ps1, then run:

.\run_check.ps1
echo $LASTEXITCODE









