# Setup Happy-Coder for Mobile
# This script will re-authenticate Happy-Coder for mobile app pairing

Write-Host ""
Write-Host "=== Happy-Coder Mobile Setup ===" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop daemon
Write-Host "[Step 1/3] Stopping daemon if running..." -ForegroundColor Yellow
happy daemon stop 2>&1 | Out-Null
Start-Sleep -Seconds 2
Write-Host "           Daemon stopped" -ForegroundColor Green

# Step 2: Re-authenticate for mobile
Write-Host ""
Write-Host "[Step 2/3] Starting authentication for mobile app..." -ForegroundColor Yellow
Write-Host "           When prompted, select: 1. Mobile App" -ForegroundColor Cyan
Write-Host "           A QR code will appear - scan it from your iPhone app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Enter to continue..." -ForegroundColor Yellow
Read-Host

happy auth login --force

# Step 3: Instructions for next step
Write-Host ""
Write-Host "[Step 3/3] After scanning QR code from your iPhone..." -ForegroundColor Yellow
Write-Host "           Run this command to start Happy-Coder:" -ForegroundColor Cyan
Write-Host "           happy" -ForegroundColor White
Write-Host ""
Write-Host "=== Keep the terminal window open while using mobile app ===" -ForegroundColor Cyan
Write-Host ""
