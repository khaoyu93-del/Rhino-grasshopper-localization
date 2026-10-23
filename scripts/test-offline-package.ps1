param([string]$RhinoRoot = 'C:\Program Files\Rhino 8')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$zip = Join-Path $root 'downloads\GrasshopperChinese-Rhino8-Pufferfish3-offline-setup.zip'
$test = Join-Path $root ('build\offline-test-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $test | Out-Null
function Invoke-Installer($folder, $libraries, $users, $packages, $state, [switch]$ExpectFailure, [string]$RhinoOverride) {
    $targetRhino = if ($RhinoOverride) { $RhinoOverride } else { $RhinoRoot }
    $arguments = @('--install','--rhino-root',$targetRhino,'--libraries',$libraries,'--user-objects',$users,'--packages',$packages,'--state',$state,'--log',(Join-Path (Split-Path $folder -Parent) 'installer-test.log'))
    $quoted = $arguments | ForEach-Object { '"' + $_ + '"' }
    $process = Start-Process -FilePath (Join-Path $folder 'Setup.exe') -ArgumentList $quoted -Wait -PassThru
    if ($ExpectFailure) { if ($process.ExitCode -eq 0) { throw 'Expected installer to reject the input.' } }
    elseif ($process.ExitCode -ne 0) { throw 'Offline installer failed.' }
}
function Invoke-Uninstaller($folder, $state) {
    $receipt = Get-Content -LiteralPath (Join-Path $state 'installation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $arguments = @('--uninstall','--state',$state,'--libraries',$receipt.libraries,'--user-objects',$receipt.userObjects,'--log',(Join-Path (Split-Path $folder -Parent) 'uninstaller-test.log'))
    $quoted = $arguments | ForEach-Object { '"' + $_ + '"' }
    $process = Start-Process -FilePath (Join-Path $folder 'Setup.exe') -ArgumentList $quoted -Wait -PassThru
    if ($process.ExitCode -ne 0) { throw 'Offline uninstall failed.' }
}
function Assert($condition, $message) { if (!$condition) { throw $message } }
try {
    Expand-Archive -LiteralPath $zip -DestinationPath (Join-Path $test 'unpacked')
    $bundle = Join-Path $test 'unpacked\GrasshopperChinese-Offline'
    $case = Join-Path $test 'fresh'
    $libraries = Join-Path $case 'Libraries'; $users = Join-Path $case 'UserObjects'; $packages = Join-Path $case 'Packages'; $state = Join-Path $case 'State'
    $existing = Join-Path $libraries 'GrasshopperChinese'
    New-Item -ItemType Directory -Path $existing -Force | Out-Null
    [IO.File]::WriteAllText((Join-Path $existing 'GrasshopperChinese.gha'), 'original-plugin')
    [IO.File]::WriteAllText((Join-Path $existing 'private.txt'), 'keep-private-file')
    Invoke-Installer $bundle $libraries $users $packages $state
    Assert (Test-Path -LiteralPath (Join-Path $libraries 'PufferfishChineseBundle\Pufferfish3-0.gha')) 'Pufferfish was not installed.'
    Assert (@(Get-ChildItem -LiteralPath $users -Filter '*.ghuser' -Recurse).Count -eq 10) 'SubD count mismatch.'
    Assert (@(Get-ChildItem -LiteralPath (Join-Path $existing 'Languages') -Filter '*.json').Count -eq 4) 'Language pack count mismatch.'
    $sdk = [Reflection.AssemblyName]::GetAssemblyName((Join-Path $RhinoRoot 'Plug-ins\Grasshopper\Grasshopper.dll')).Version
    $installed = [Reflection.Assembly]::Load([IO.File]::ReadAllBytes((Join-Path $existing 'GrasshopperChinese.gha')))
    Assert (($installed.GetReferencedAssemblies() | Where-Object Name -eq 'Grasshopper').Version -eq $sdk) 'Installed plugin does not reference target SDK.'
    $hashes = @{}
    $receipt = Get-Content -LiteralPath (Join-Path $state 'installation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($file in $receipt.files) { $hashes[$file.target] = $file.installedHash }
    $receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $state 'installation.json') -Encoding UTF8
    Invoke-Installer $bundle $libraries $users $packages $state
    $repeat = Get-Content -LiteralPath (Join-Path $state 'installation.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert ($repeat.files.Count -eq $receipt.files.Count) 'Repeated install created duplicate records.'
    Assert (@(Get-ChildItem -LiteralPath $users -Filter '*.ghuser' -Recurse).Count -eq 10) 'Repeated install duplicated SubD objects.'
    Invoke-Uninstaller $bundle $state
    Assert ([IO.File]::ReadAllText((Join-Path $existing 'GrasshopperChinese.gha')) -eq 'original-plugin') 'Original plugin was not restored.'
    Assert ([IO.File]::ReadAllText((Join-Path $existing 'private.txt')) -eq 'keep-private-file') 'Private file was changed.'
    Assert (!(Test-Path -LiteralPath (Join-Path $libraries 'PufferfishChineseBundle\Pufferfish3-0.gha'))) 'Bundled Pufferfish was not removed.'
    Assert (@(Get-ChildItem -LiteralPath $users -Filter '*.ghuser' -Recurse).Count -eq 0) 'Bundled SubD objects were not removed.'
    Write-Host 'PASS standalone EXE offline compilation, first/repeated install and original-file restoration'

    $case = Join-Path $test 'external'
    $libraries = Join-Path $case 'Libraries'; $users = Join-Path $case 'UserObjects'; $packages = Join-Path $case 'Packages'; $state = Join-Path $case 'State'
    New-Item -ItemType Directory -Path (Join-Path $packages 'Pufferfish\3.0.0') -Force | Out-Null
    New-Item -ItemType Directory -Path $users -Force | Out-Null
    $external = Join-Path $packages 'Pufferfish\3.0.0\Pufferfish3-0.gha'
    Copy-Item -LiteralPath (Join-Path $bundle 'Pufferfish\Pufferfish3-0.gha') -Destination $external
    $subd = Get-ChildItem -LiteralPath (Join-Path $bundle 'Pufferfish\SubD') -File | Select-Object -First 1
    Copy-Item -LiteralPath $subd.FullName -Destination (Join-Path $users $subd.Name)
    Invoke-Installer $bundle $libraries $users $packages $state
    Assert (!(Test-Path -LiteralPath (Join-Path $libraries 'PufferfishChineseBundle\Pufferfish3-0.gha'))) 'External Pufferfish was duplicated.'
    Assert (@(Get-ChildItem -LiteralPath $users -Filter '*.ghuser' -Recurse).Count -eq 10) 'External SubD was duplicated.'
    Invoke-Uninstaller $bundle $state
    Assert (Test-Path -LiteralPath $external) 'External Pufferfish was removed.'
    Assert (@(Get-ChildItem -LiteralPath $users -Filter '*.ghuser' -Recurse).Count -eq 1) 'External SubD object was removed.'
    Write-Host 'PASS existing Pufferfish and identical SubD reuse without removal'

    $case = Join-Path $test 'invalid-sdk'
    Invoke-Installer $bundle (Join-Path $case 'Libraries') (Join-Path $case 'UserObjects') (Join-Path $case 'Packages') (Join-Path $case 'State') -ExpectFailure -RhinoOverride (Join-Path $case 'no-rhino')
    Assert (!(Test-Path -LiteralPath (Join-Path $case 'Libraries'))) 'Missing Rhino wrote installation files.'
    Write-Host 'PASS missing Rhino SDK rejection without target-file changes'

    $case = Join-Path $test 'corrupt'
    Copy-Item -LiteralPath $bundle -Destination (Join-Path $case 'bundle') -Recurse
    $corrupt = Join-Path $case 'bundle'
    [IO.File]::AppendAllText((Join-Path $corrupt 'src\Plugin.cs'), 'corrupted')
    Invoke-Installer $corrupt (Join-Path $case 'Libraries') (Join-Path $case 'Users') (Join-Path $case 'Packages') (Join-Path $case 'State') -ExpectFailure
    Assert (!(Test-Path -LiteralPath (Join-Path $case 'Libraries'))) 'Corrupt package wrote installation files.'
    Write-Host 'PASS integrity rejection before installation'

    $case = Join-Path $test 'compiler-failure'
    $modifiedBundle = Join-Path $case 'bundle'
    Copy-Item -LiteralPath $bundle -Destination $modifiedBundle -Recurse
    $sourcePath = Join-Path $modifiedBundle 'src\Plugin.cs'
    [IO.File]::AppendAllText($sourcePath, ' invalid C sharp source')
    $manifestPath = Join-Path $modifiedBundle 'package-manifest.json'
    $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    ($manifest.files | Where-Object path -eq 'src\Plugin.cs').sha256 = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
    $manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding UTF8
    Invoke-Installer $modifiedBundle (Join-Path $case 'Libraries') (Join-Path $case 'UserObjects') (Join-Path $case 'Packages') (Join-Path $case 'State') -ExpectFailure
    Assert (!(Test-Path -LiteralPath (Join-Path $case 'Libraries'))) 'Compiler failure changed target installation.'
    Write-Host 'PASS SDK compilation failure stops before file replacement'

    $case = Join-Path $test 'conflict'
    $libraries = Join-Path $case 'Libraries'; $users = Join-Path $case 'UserObjects'; $packages = Join-Path $case 'Packages'; $state = Join-Path $case 'State'
    New-Item -ItemType Directory -Path $users -Force | Out-Null
    [IO.File]::WriteAllText((Join-Path $users $subd.Name), 'personal-subd-edit')
    Invoke-Installer $bundle $libraries $users $packages $state -ExpectFailure
    Assert ([IO.File]::ReadAllText((Join-Path $users $subd.Name)) -eq 'personal-subd-edit') 'Conflicting SubD was overwritten.'
    Assert (!(Test-Path -LiteralPath $libraries)) 'Conflict wrote installation files.'
    Write-Host 'PASS personal SubD conflict protection'

    $case = Join-Path $test 'rollback'
    $libraries = Join-Path $case 'Libraries'; $users = Join-Path $case 'UserObjects'; $packages = Join-Path $case 'Packages'; $state = Join-Path $case 'State'
    $existing = Join-Path $libraries 'GrasshopperChinese'
    New-Item -ItemType Directory -Path $existing -Force | Out-Null
    $lockedPath = Join-Path $existing 'README.md'
    [IO.File]::WriteAllText($lockedPath, 'original-readme')
    $lock = [IO.File]::Open($lockedPath,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
    try { Invoke-Installer $bundle $libraries $users $packages $state -ExpectFailure }
    finally { $lock.Dispose() }
    Assert ([IO.File]::ReadAllText($lockedPath) -eq 'original-readme') 'Failed copy changed the locked original file.'
    Assert (@(Get-ChildItem -LiteralPath $existing -Filter '*.json' -Recurse).Count -eq 0) 'Failed copy did not roll back new dictionaries.'
    Assert (!(Test-Path -LiteralPath (Join-Path $state 'installation.json'))) 'Failed copy wrote a successful receipt.'
    Write-Host 'PASS copy failure rollback preserves locked original and removes newly copied files'

    $case = Join-Path $test 'modified'
    $libraries = Join-Path $case 'Libraries'; $users = Join-Path $case 'UserObjects'; $packages = Join-Path $case 'Packages'; $state = Join-Path $case 'State'
    Invoke-Installer $bundle $libraries $users $packages $state
    $edited = Join-Path $libraries 'GrasshopperChinese\Languages\pufferfish.zh-CN.json'
    [IO.File]::AppendAllText($edited, 'personal-edit')
    $editedHash = (Get-FileHash -LiteralPath $edited -Algorithm SHA256).Hash
    Invoke-Uninstaller $bundle $state
    Assert ((Get-FileHash -LiteralPath $edited -Algorithm SHA256).Hash -eq $editedHash) 'Uninstall deleted or overwrote a personal dictionary edit.'
    Assert (Test-Path -LiteralPath (Join-Path $state 'installation.json')) 'Modified file receipt was not retained.'
    Write-Host 'PASS uninstall preserves personal dictionary edits and their receipt'

    $case = Join-Path $test '异地 安装 路径'
    $relocated = Join-Path $case '离线 包'
    Copy-Item -LiteralPath $bundle -Destination $relocated -Recurse
    $libraries = Join-Path $case '用户 组件'; $users = Join-Path $case '用户 对象'; $packages = Join-Path $case '其他 插件'; $state = Join-Path $case '安装 记录'
    Invoke-Installer $relocated $libraries $users $packages $state
    Assert (Test-Path -LiteralPath (Join-Path $libraries 'GrasshopperChinese\GrasshopperChinese.gha')) 'Relocated Unicode/spaced path failed.'
    Invoke-Uninstaller $relocated $state
    Write-Host 'PASS relocated offline bundle and Unicode/spaced paths'
} finally {
    if (Test-Path -LiteralPath $test) { Remove-Item -LiteralPath $test -Recurse -Force }
}
