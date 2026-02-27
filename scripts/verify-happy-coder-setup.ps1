# Happy-Coder Setup Verification Script
# Run this from PowerShell to check your setup

Write-Host ""
Write-Host "=== Happy-Coder Setup Verification ===" -ForegroundColor Cyan
Write-Host "Checking your configuration..." -ForegroundColor Cyan
Write-Host ""

# Check 1: ANTHROPIC_API_KEY (should NOT be set)
Write-Host "[1/7] Checking ANTHROPIC_API_KEY..." -NoNewline
if ($env:ANTHROPIC_API_KEY) {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "      WARNING: API key is set! You'll be charged API credits instead of using subscription." -ForegroundColor Yellow
    Write-Host "      Remove it with:" -ForegroundColor Yellow
    Write-Host "      [System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', `$null, 'User')" -ForegroundColor Yellow
} else {
    Write-Host " PASS" -ForegroundColor Green
    Write-Host "      Using Claude Max subscription tokens (saves thousands per month!)" -ForegroundColor Gray
}

# Check 2: GITHUB_TOKEN (should be set)
Write-Host ""
Write-Host "[2/7] Checking GITHUB_TOKEN..." -NoNewline
if ($env:GITHUB_TOKEN) {
    $tokenPreview = $env:GITHUB_TOKEN.Substring(0, [Math]::Min(10, $env:GITHUB_TOKEN.Length))
    Write-Host " PASS" -ForegroundColor Green
    Write-Host "      Token is set (first 10 chars: ${tokenPreview}...)" -ForegroundColor Gray
} else {
    Write-Host " WARN" -ForegroundColor Yellow
    Write-Host "      No GitHub token set. You won't be able to push changes." -ForegroundColor Gray
    Write-Host "      Set it with:" -ForegroundColor Gray
    Write-Host "      [System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'your-token', 'User')" -ForegroundColor Gray
}

# Check 3: Happy-Coder installation
Write-Host ""
Write-Host "[3/7] Checking Happy-Coder installation..." -NoNewline
try {
    $happyVersion = & happy --version 2>&1 | Select-String "happy version" | ForEach-Object { $_.ToString() }
    if ($happyVersion -match "happy version: (.+)") {
        Write-Host " PASS" -ForegroundColor Green
        Write-Host "      Installed version: $($Matches[1].Trim())" -ForegroundColor Gray
    } else {
        Write-Host " UNKNOWN" -ForegroundColor Yellow
        Write-Host "      Could not determine version" -ForegroundColor Gray
    }
} catch {
    Write-Host " FAIL" -ForegroundColor Red
    Write-Host "      Happy-Coder not found. Install with: npm i -g happy-coder" -ForegroundColor Gray
}

# Check 4: Happy-Coder authentication
Write-Host ""
Write-Host "[4/7] Checking Happy-Coder authentication..." -NoNewline
try {
    $authStatus = & happy auth status 2>&1 | Out-String
    if ($authStatus -match "Not authenticated") {
        Write-Host " WARN" -ForegroundColor Yellow
        Write-Host "      Not authenticated yet. Run: happy auth login" -ForegroundColor Gray
    } elseif ($authStatus -match "Authenticated") {
        Write-Host " PASS" -ForegroundColor Green
        Write-Host "      Ready to use!" -ForegroundColor Gray
    } else {
        Write-Host " UNKNOWN" -ForegroundColor Yellow
        Write-Host "      Could not determine auth status. Run: happy auth status" -ForegroundColor Gray
    }
} catch {
    Write-Host " ERROR" -ForegroundColor Red
    Write-Host "      Could not check auth status" -ForegroundColor Gray
}

# Check 5: Skills directory
Write-Host ""
Write-Host "[5/7] Checking skills directory..." -NoNewline
$skillsPath = "$env:USERPROFILE\.claude\skills"
if (Test-Path $skillsPath) {
    $skillCount = (Get-ChildItem $skillsPath -Directory -ErrorAction SilentlyContinue).Count
    Write-Host " PASS" -ForegroundColor Green
    Write-Host "      Found $skillCount skills in: $skillsPath" -ForegroundColor Gray
} else {
    Write-Host " WARN" -ForegroundColor Yellow
    Write-Host "      Skills directory not found at: $skillsPath" -ForegroundColor Gray
}

# Check 6: CLAUDE.md
Write-Host ""
Write-Host "[6/7] Checking CLAUDE.md..." -NoNewline
$claudeMdPath = "$env:USERPROFILE\.claude\CLAUDE.md"
if (Test-Path $claudeMdPath) {
    $lineCount = (Get-Content $claudeMdPath -ErrorAction SilentlyContinue).Count
    Write-Host " PASS" -ForegroundColor Green
    Write-Host "      Global config found: $lineCount lines" -ForegroundColor Gray
} else {
    Write-Host " WARN" -ForegroundColor Yellow
    Write-Host "      CLAUDE.md not found at: $claudeMdPath" -ForegroundColor Gray
}

# Check 7: Repositories directory
Write-Host ""
Write-Host "[7/7] Checking repositories directory..." -NoNewline
$reposPath = "C:\Repositories for Git"
if (Test-Path $reposPath) {
    $repoCount = (Get-ChildItem $reposPath -Directory -ErrorAction SilentlyContinue).Count
    Write-Host " PASS" -ForegroundColor Green
    Write-Host "      Found $repoCount repositories in: $reposPath" -ForegroundColor Gray
} else {
    Write-Host " WARN" -ForegroundColor Yellow
    Write-Host "      Repositories directory not found at: $reposPath" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
$happyInstalled = (Get-Command happy -ErrorAction SilentlyContinue) -ne $null
if (-not $env:ANTHROPIC_API_KEY -and $env:GITHUB_TOKEN -and $happyInstalled) {
    Write-Host "Your setup looks good!" -ForegroundColor Green
    try {
        $authCheck = & happy auth status 2>&1 | Out-String
        if ($authCheck -match "Not authenticated") {
            Write-Host ""
            Write-Host "Next step: Run 'happy auth login' to authenticate" -ForegroundColor Yellow
        } else {
            Write-Host ""
            Write-Host "You're ready to use Happy-Coder from your iPhone!" -ForegroundColor Green
            Write-Host "Start with: happy" -ForegroundColor Cyan
        }
    } catch {
        Write-Host ""
        Write-Host "Next step: Authenticate with 'happy auth login'" -ForegroundColor Yellow
    }
} else {
    Write-Host "Some issues detected. Review the checks above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Quick Actions ===" -ForegroundColor Cyan
Write-Host "Authenticate:           happy auth login" -ForegroundColor Gray
Write-Host "Start Happy-Coder:      happy" -ForegroundColor Gray
Write-Host "Resume session:         happy --resume" -ForegroundColor Gray
Write-Host "Check authentication:   happy auth status" -ForegroundColor Gray
Write-Host "Run diagnostics:        happy doctor" -ForegroundColor Gray

Write-Host ""
Write-Host "=== Documentation ===" -ForegroundColor Cyan
Write-Host "Full setup guide:       $env:USERPROFILE\.claude\scripts\happy-coder-setup-guide.md" -ForegroundColor Gray
Write-Host "Quick reference:        $env:USERPROFILE\.claude\scripts\happy-coder-quick-reference.md" -ForegroundColor Gray

Write-Host ""
