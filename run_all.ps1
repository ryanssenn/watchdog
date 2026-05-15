# run_all.ps1
$python = "c:\python314\python.exe"

$pairs = @(
  @{ base=".\fp16_base_chat_c16.json"; test=".\fp8_base_chat_c16.json"; name="chat" }
  # Add more pairs here later
)

foreach ($p in $pairs) {
  Write-Host "=== Checking $($p.name) ==="
  & $python .\check_regressions.py $p.base $p.test

  if ($LASTEXITCODE -ne 0) {
    Write-Host "STOP: $($p.name) failed (exit code=$LASTEXITCODE)"
    exit $LASTEXITCODE
  }
}

Write-Host "ALL PASSED"
exit 0
