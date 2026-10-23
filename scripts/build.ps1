param([string]$RhinoRoot = 'C:\Program Files\Rhino 8')
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$source = Get-Content -LiteralPath "$root\src\Plugin.cs" -Raw
$menu = [regex]::Match($source, '(?s)static readonly Dictionary<string, string> menuText = .*?\{(.*?)\n\s*\};')
if (!$menu.Success) { throw 'Menu dictionary not found' }
$seen = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::OrdinalIgnoreCase)
foreach ($entry in [regex]::Matches($menu.Groups[1].Value, '\{\s*"([^"\r\n]+)"\s*,\s*"')) {
    if (!$seen.Add($entry.Groups[1].Value)) { throw "Duplicate menu key: $($entry.Groups[1].Value)" }
}
foreach ($pack in @('zh-CN.json', 'tool-text.zh-CN.json', 'pufferfish.zh-CN.json', 'pufferfish-text.zh-CN.json')) {
    $rows = Get-Content -LiteralPath "$root\Languages\$pack" -Raw | ConvertFrom-Json
    $entries = New-Object 'System.Collections.Generic.HashSet[string]' ([System.StringComparer]::Ordinal)
    foreach ($row in $rows) {
        if (!$row.name -or !$row.translation) { throw "Incomplete entry in $pack" }
        $key = "$($row.category)|$($row.name)"
        if (!$entries.Add($key)) { throw "Duplicate translation in ${pack}: $($row.category)/$($row.name)" }
    }
}
$out = Join-Path $root 'build\GrasshopperChinese'
New-Item -ItemType Directory -Force -Path $out | Out-Null
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$refs = @('System.Drawing.dll', 'System.Windows.Forms.dll', 'System.Runtime.Serialization.dll', (Join-Path (Split-Path $compiler -Parent) 'netstandard.dll'), "$RhinoRoot\System\Eto.dll", "$RhinoRoot\System\RhinoCommon.dll", "$RhinoRoot\Plug-ins\Grasshopper\Grasshopper.dll", "$RhinoRoot\Plug-ins\Grasshopper\GH_IO.dll")
$arguments = @('/nologo', '/utf8output', '/target:library', '/optimize+', '/platform:anycpu', "/out:$out\GrasshopperChinese.gha")
$arguments += $refs | ForEach-Object { '/r:' + $_ }
$arguments += @("$root\src\Core.cs", "$root\src\Plugin.cs", "$root\src\RibbonTranslator.cs")
& $compiler $arguments
if ($LASTEXITCODE -ne 0) { throw 'Plugin compilation failed' }
Copy-Item -LiteralPath "$root\Languages" -Destination $out -Recurse -Force
Copy-Item -LiteralPath "$root\LICENSE-MultilingualGH.txt", "$root\THIRD-PARTY-NOTICES.md", "$root\README.md" -Destination $out -Force
Write-Host "Built $out\GrasshopperChinese.gha"
