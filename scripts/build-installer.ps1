$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$out = Join-Path $root 'build\Setup.exe'
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
& $compiler /nologo /utf8output /target:winexe /optimize+ /platform:anycpu "/out:$out" /r:System.Drawing.dll /r:System.Windows.Forms.dll /r:System.Runtime.Serialization.dll /r:System.Core.dll "$root\installer\Setup.cs" "$root\src\Core.cs"
if ($LASTEXITCODE -ne 0) { throw 'Standalone installer compilation failed.' }
Write-Host "Built $out"
