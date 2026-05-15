# run_check_switch.ps1
$python = "c:\python314\python.exe"

& $python .\check_regressions.py .\fp16_base_chat_c16.json .\fp8_base_chat_c16.json

switch ($LASTEXITCODE) {
  0 { "PASSED (no regressions)"; exit 0 }
  1 { "FAILED (regression detected)"; exit 1 }
  2 { "ERROR (missing args / usage)"; exit 2 }
  default { "ERROR (unexpected exit code: $LASTEXITCODE)"; exit $LASTEXITCODE }
}