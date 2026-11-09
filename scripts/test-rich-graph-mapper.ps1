param(
    [string]$PluginPath,
    [string]$RichPluginPath = (Join-Path $env:APPDATA 'Grasshopper\Libraries\RichedGraphMapperRhino8\RichedGraphMapper.gha'),
    [string]$RhinoRoot = 'C:\Program Files\Rhino 8'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$plugin = if ($PluginPath) { $PluginPath } else { Join-Path $root 'build\GrasshopperChinese\GrasshopperChinese.gha' }
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$test = Join-Path $root 'build\RichGraphMapperTests.dll'
$references = @('System.dll', 'System.Core.dll', 'System.Drawing.dll', 'System.Windows.Forms.dll', $plugin, (Join-Path $RhinoRoot 'System\RhinoCommon.dll'), (Join-Path $RhinoRoot 'Plug-ins\Grasshopper\Grasshopper.dll'), (Join-Path $RhinoRoot 'Plug-ins\Grasshopper\GH_IO.dll'))
$arguments = @('/nologo', '/utf8output', '/target:library', "/out:$test")
$arguments += $references | ForEach-Object { '/r:' + $_ }
$arguments += Join-Path $root 'tests\RichGraphMapperTests.cs'
& $compiler $arguments
if ($LASTEXITCODE -ne 0) { throw 'Rich Graph Mapper test compilation failed.' }
if ($PSVersionTable.PSEdition -eq 'Desktop') { throw 'Run these offline SDK resource tests with PowerShell 7; no installation or policy changes are performed.' }
foreach ($relative in @('System\System.Resources.Extensions.dll', 'System\Eto.dll', 'System\RhinoCommon.dll', 'Plug-ins\Grasshopper\GH_IO.dll', 'Plug-ins\Grasshopper\Grasshopper.dll')) {
    $null = [Reflection.Assembly]::LoadFrom((Join-Path $RhinoRoot $relative))
}
$null = [Reflection.Assembly]::LoadFrom($plugin)
$null = [Reflection.Assembly]::LoadFrom($RichPluginPath)
$assembly = [Reflection.Assembly]::Load([IO.File]::ReadAllBytes($test))
$parameters = New-Object 'object[]' 1
$parameters[0] = [string]$root
try { $assembly.GetType('RichGraphMapperTests').GetMethod('Run').Invoke($null, $parameters) }
catch {
    $failure = $_.Exception
    while ($failure.InnerException) { $failure = $failure.InnerException }
    [Console]::Error.WriteLine($failure.ToString())
    throw
}
