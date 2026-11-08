$ErrorActionPreference = "Stop"

$projectRoot = $PSScriptRoot
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$pythonw = Join-Path $projectRoot ".venv\Scripts\pythonw.exe"
$supervisor = Join-Path $projectRoot "server_supervisor.py"
$taskName = "Career Compass"
$identity = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

if (-not (Test-Path $python)) {
    throw "The project Python environment is missing: $python"
}
if (-not (Test-Path $pythonw)) {
    throw "The project windowless Python executable is missing: $pythonw"
}
if (-not (Test-Path $supervisor)) {
    throw "The startup supervisor is missing: $supervisor"
}

$action = New-ScheduledTaskAction -Execute $pythonw -Argument "`"$supervisor`""
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $identity
$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) -StartWhenAvailable `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -Hidden

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger `
    -Principal $principal -Settings $settings `
    -Description "Starts and monitors the local Career Compass website when this user signs in." `
    -Force | Out-Null
Start-ScheduledTask -TaskName $taskName

$desktopShortcut = Join-Path ([Environment]::GetFolderPath("Desktop")) "Career Compass.url"
Set-Content -Path $desktopShortcut -Value "[InternetShortcut]`r`nURL=http://127.0.0.1:5050/`r`n"

$deadline = (Get-Date).AddSeconds(45)
do {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:5050/login" `
            -UseBasicParsing -TimeoutSec 3
        if ($response.StatusCode -eq 200 -and $response.Content.Contains("Career Compass")) {
            Write-Host "Career Compass is running at http://127.0.0.1:5050/"
            Write-Host "Automatic startup is registered for $identity."
            Write-Host "Desktop shortcut: $desktopShortcut"
            exit 0
        }
    }
    catch {
        $lastStartupError = $_.Exception.Message
    }
    Start-Sleep -Seconds 1
} while ((Get-Date) -lt $deadline)

$errorLog = Join-Path $projectRoot "logs\server-error.log"
throw "The startup task was registered, but Career Compass did not become ready. See $errorLog. Last connection error: $lastStartupError"
