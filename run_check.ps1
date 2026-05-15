# run_check.ps1
# Run the regression check and fail the script if regressions are found.

$python = "c:\python314\python.exe"
$script = ".\check_regressions.py"
$base   = ".\fp16_base_chat_c16.json"
$test   = ".\fp8_base_chat_c16.json"

& $python $script $base $test

Write-Host "Exit code: $LASTEXITCODE"

if ($LASTEXITCODE -eq 0) {
  Write-Host "PASSED (no regressions)"
  exit 0
}
elseif ($LASTEXITCODE -eq 1) {
  Write-Host "FAILED (regression detected)"
  exit 1
}
elseif ($LASTEXITCODE -eq 2) {
  Write-Host "ERROR (usage / missing args)"
  exit 2
}
else {
  Write-Host "ERROR (unexpected exit code: $LASTEXITCODE)"
  exit $LASTEXITCODE
}