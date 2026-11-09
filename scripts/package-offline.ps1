param(
    [string]$RhinoRoot = 'C:\Program Files\Rhino 8',
    [string]$PufferfishRoot = (Join-Path $env:APPDATA 'McNeel\Rhinoceros\packages\8.0\Pufferfish\3.0.0'),
    [string]$OutputName = 'GrasshopperChinese-0.3.1-Rhino8-Pufferfish3-RichedGraphMapper-tab-offline-setup.zip'
)
$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($OutputName) -or [IO.Path]::IsPathRooted($OutputName) -or $OutputName.IndexOfAny([IO.Path]::GetInvalidFileNameChars()) -ge 0 -or $OutputName.Contains('/') -or $OutputName.Contains('\') -or $OutputName.Contains(':') -or [IO.Path]::GetExtension($OutputName) -ne '.zip' -or [string]::IsNullOrWhiteSpace([IO.Path]::GetFileNameWithoutExtension($OutputName))) { throw 'OutputName must be a single ZIP filename without a directory.' }
$root = Split-Path $PSScriptRoot -Parent
$build = Join-Path $root 'build\GrasshopperChinese'
$outputRoot = Join-Path $root 'downloads'
if (!(Test-Path -LiteralPath $outputRoot -PathType Container)) { throw 'Package output directory is missing.' }
$zipName = $OutputName
$zip = Join-Path $outputRoot $zipName
if ((Test-Path -LiteralPath $zip) -or (Test-Path -LiteralPath ($zip + '.sha256'))) { throw 'Offline ZIP or checksum already exists; preserve or move it before building another package.' }
$fish = Join-Path $PufferfishRoot 'Pufferfish3-0.gha'
if (!(Test-Path -LiteralPath $fish -PathType Leaf)) { throw 'Original Pufferfish 3.0 plugin is missing.' }
$fishAssembly = [Reflection.AssemblyName]::GetAssemblyName($fish)
if ($fishAssembly.Name -ne 'Pufferfish' -or $fishAssembly.Version.ToString() -ne '3.0.0.0') { throw 'Expected original Pufferfish 3.0.0.0.' }
$users = @(Get-ChildItem -LiteralPath (Join-Path $PufferfishRoot 'Pufferfish WIP SubD Components') -Filter '*.ghuser' -File)
if ($users.Count -ne 10) { throw 'Expected ten original Pufferfish SubD user objects.' }
$null = & (Join-Path $PSScriptRoot 'build.ps1') -RhinoRoot $RhinoRoot
if ($LASTEXITCODE -ne 0) { throw 'Localization build failed.' }
$null = & (Join-Path $PSScriptRoot 'build-installer.ps1')
if ($LASTEXITCODE -ne 0) { throw 'Standalone installer build failed.' }
$stage = Join-Path $outputRoot ('offline-stage-' + [Guid]::NewGuid().ToString('N'))
$bundle = Join-Path $stage 'GrasshopperChinese-Offline'
New-Item -ItemType Directory -Path $bundle -Force | Out-Null
try {
    foreach ($folder in @('src','Languages','GrasshopperChinese','Pufferfish\SubD')) { New-Item -ItemType Directory -Path (Join-Path $bundle $folder) -Force | Out-Null }
    Copy-Item -LiteralPath (Join-Path $root 'build\Setup.exe') -Destination (Join-Path $bundle 'Setup.exe')
    foreach ($name in @('Core.cs','Plugin.cs','RibbonTranslator.cs')) { Copy-Item -LiteralPath (Join-Path $root "src\$name") -Destination (Join-Path $bundle "src\$name") }
    foreach ($name in @('zh-CN.json','tool-text.zh-CN.json','pufferfish.zh-CN.json','pufferfish-text.zh-CN.json','richedgraphmapper.zh-CN.json')) { Copy-Item -LiteralPath (Join-Path $root "Languages\$name") -Destination (Join-Path $bundle "Languages\$name") }
    Copy-Item -LiteralPath (Join-Path $build 'GrasshopperChinese.gha') -Destination (Join-Path $bundle 'GrasshopperChinese\GrasshopperChinese.gha')
    Copy-Item -LiteralPath $fish -Destination (Join-Path $bundle 'Pufferfish\Pufferfish3-0.gha')
    Copy-Item -LiteralPath (Join-Path $PufferfishRoot 'READ ME FIRST_Pufferfish Installation and Notes.txt') -Destination (Join-Path $bundle 'Pufferfish\AUTHOR-NOTES.txt')
    foreach ($file in $users) { Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $bundle 'Pufferfish\SubD') }
    foreach ($name in @('README.md','THIRD-PARTY-NOTICES.md','LICENSE-MultilingualGH.txt')) { Copy-Item -LiteralPath (Join-Path $root $name) -Destination (Join-Path $bundle $name) }
    $files = @(Get-ChildItem -LiteralPath $bundle -Recurse -File | Sort-Object FullName | ForEach-Object {
        @{path=$_.FullName.Substring($bundle.Length).TrimStart('\');sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
    })
    @{format=1;package=[IO.Path]::GetFileNameWithoutExtension($zipName);createdAt=(Get-Date).ToString('o');referenceSdk=[Reflection.AssemblyName]::GetAssemblyName((Join-Path $RhinoRoot 'Plug-ins\Grasshopper\Grasshopper.dll')).Version.ToString();files=$files} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $bundle 'package-manifest.json') -Encoding UTF8
    Compress-Archive -LiteralPath $bundle -DestinationPath $zip -CompressionLevel Optimal
    $hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
    [IO.File]::WriteAllText($zip + '.sha256', "$hash  $zipName`r`n", [Text.Encoding]::ASCII)
    Write-Host "Package: $zip"
    Write-Host "SHA256: $hash"
    Write-Host "Files: $($files.Count + 1); SDK and Rhino binaries not included."
} finally {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
}
