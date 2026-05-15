# run_check_chain.ps1  (PowerShell 7+)
$python = "c:\python314\python.exe"

& $python .\check_regressions.py .\fp16_base_chat_c16.json .\fp8_base_chat_c16.json &&
  (Write-Host "PASSED (no regressions)"; exit 0) ||
  (Write-Host "FAILED/ERROR (exit code=$LASTEXITCODE)"; exit $LASTEXITCODE)
``