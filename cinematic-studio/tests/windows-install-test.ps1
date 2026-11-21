# Installs the app silently, starts it, checks that it created the user's library and that the interface
# reached the core, restarts it, uninstalls it, and checks that the user's projects were left alone.
# Run on Windows 10/11:  pwsh tests/windows-install-test.ps1 -Installer path\to\Cinematic Studio_0.1.0_x64-setup.exe
param([Parameter(Mandatory)][string]$Installer)
$ErrorActionPreference = 'Stop'
$failed = 0
function Check([string]$name, [bool]$ok) { if ($ok) { "  ok   $name" } else { "  FAIL $name"; $script:failed++ } }
function WaitFor([scriptblock]$cond, [int]$seconds) { for ($i = 0; $i -lt $seconds * 2; $i++) { if (& $cond) { return $true }; Start-Sleep -Milliseconds 500 }; return $false }

$docs = [Environment]::GetFolderPath('MyDocuments')
$library = Join-Path $docs 'Cinematic Studio'
$startMenu = Join-Path ([Environment]::GetFolderPath('Programs')) 'Cinematic Studio'
$desktop = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Cinematic Studio.lnk'
$uninstallKey = 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\Cinematic Studio'

"Installing $Installer"
$p = Start-Process -FilePath $Installer -ArgumentList '/S' -Wait -PassThru
Check 'installer exits with code 0' ($p.ExitCode -eq 0)
Check 'uninstall entry registered for the current user' (Test-Path $uninstallKey)
$installDir = (Get-ItemProperty $uninstallKey -ErrorAction SilentlyContinue).InstallLocation
if ($installDir) { $installDir = $installDir.Trim('"') }
"Install folder: $installDir"
$exe = if ($installDir) { Get-ChildItem $installDir -Filter '*.exe' | Where-Object { $_.Name -notmatch 'uninstall' } | Select-Object -First 1 } else { $null }
Check 'application executable installed' ($null -ne $exe)
Check 'FFmpeg bundled with the app' ($installDir -and (Get-ChildItem $installDir -Recurse -Filter 'ffmpeg.exe' -ErrorAction SilentlyContinue).Count -ge 1)
$startLnk = Get-ChildItem ([Environment]::GetFolderPath('Programs')) -Recurse -Filter 'Cinematic Studio.lnk' -ErrorAction SilentlyContinue | Select-Object -First 1
Check 'Start menu shortcut' ($null -ne $startLnk)
Check 'desktop shortcut' (Test-Path $desktop)
if ($startLnk) { $target = (New-Object -ComObject WScript.Shell).CreateShortcut($startLnk.FullName).TargetPath; Check 'shortcut points at the installed executable' ($exe -and $target -eq $exe.FullName) }
if (-not $exe) { "Cannot continue without the executable."; exit 1 }

"First launch"
$app = Start-Process -FilePath $exe.FullName -PassThru
Check 'library folders created in Documents' (WaitFor { @('Projects','Assets','Models','Cache','Logs','Backups') | ForEach-Object { Test-Path (Join-Path $library $_) } | Where-Object { -not $_ } | Measure-Object | ForEach-Object { $_.Count -eq 0 } } 60)
Check 'database created' (WaitFor { Test-Path (Join-Path $library 'cinematic-studio.db') } 30)
Check 'the interface loaded and reached the core' (WaitFor { Test-Path (Join-Path $library 'Logs\ui-connected.txt') } 90)
$selfCheck = Join-Path $library 'Logs\self-check.json'
if (WaitFor { Test-Path $selfCheck } 60) {
  $sc = Get-Content $selfCheck -Raw | ConvertFrom-Json
  Check 'the bundled FFmpeg rendered a test clip on this machine' ($sc.ffmpeg_ok -eq $true)
  Check 'the app read a file of the library through its own file scheme' ($sc.image_ok -eq $true)
  Check 'the app showed that clip in its own video player (H.264 through the studio scheme)' ($sc.video_ok -eq $true)
  "       web view: $($sc.detail)"
} else { Check 'self-check report written' $false }
Check 'process still running after start' (-not $app.HasExited)
$second = Start-Process -FilePath $exe.FullName -PassThru
Check 'a second copy does not stay open (single instance)' (WaitFor { $second.HasExited } 30)

# a file standing in for the user's work, to prove uninstall leaves it alone
$marker = Join-Path $library 'Projects\keep-me\project.json'
New-Item -ItemType Directory -Force (Split-Path $marker) | Out-Null
Set-Content $marker '{"name":"user project"}'

"Closing and restarting"
$app.Refresh()
[void]$app.CloseMainWindow()
if (-not (WaitFor { $app.HasExited } 20)) { "  note: window did not close on request; ending the process"; Stop-Process -Id $app.Id -Force }
Remove-Item (Join-Path $library 'Logs\ui-connected.txt') -ErrorAction SilentlyContinue
$app = Start-Process -FilePath $exe.FullName -PassThru
Check 'starts again after restart' (WaitFor { Test-Path (Join-Path $library 'Logs\ui-connected.txt') } 90)
Check 'user file still present after restart' (Test-Path $marker)
[void]$app.CloseMainWindow()
if (-not (WaitFor { $app.HasExited } 20)) { Stop-Process -Id $app.Id -Force }
Get-Process | Where-Object { $_.Path -eq $exe.FullName } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

"Uninstalling"
$un = Join-Path $installDir 'uninstall.exe'
Check 'uninstaller present' (Test-Path $un)
if (Test-Path $un) {
  # NSIS copies its uninstaller to a temp folder and returns unless _?= is given
  $u = Start-Process -FilePath $un -ArgumentList '/S', "_?=$installDir" -Wait -PassThru
  Check 'uninstaller exits with code 0' ($u.ExitCode -eq 0)
}
Check 'application executable removed' (-not (Test-Path $exe.FullName))
Check 'Start menu shortcut removed' (-not ($startLnk -and (Test-Path $startLnk.FullName)))
Check 'desktop shortcut removed' (-not (Test-Path $desktop))
Check 'uninstall entry removed' (-not (Test-Path $uninstallKey))
Check 'user projects kept after uninstall' ((Test-Path $marker) -and (Test-Path (Join-Path $library 'cinematic-studio.db')))

if ($failed) { "`n$failed check(s) failed"; exit 1 } else { "`nAll install checks passed"; exit 0 }
