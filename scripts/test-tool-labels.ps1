param([string]$PluginPath)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$env:GRASSHOPPER_CHINESE_TEST_ROOT = $root
$compiler = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
$sdk = 'C:\Program Files\Rhino 8\Plug-ins\Grasshopper\Grasshopper.dll'
$plugin = if ($PluginPath) { $PluginPath } else { "$root\build\GrasshopperChinese\GrasshopperChinese.gha" }
$testAssembly = Join-Path $env:TEMP ('GrasshopperChinese-tool-label-tests-' + [Guid]::NewGuid().ToString('N') + '.dll')
& $compiler /nologo /utf8output /target:library "/out:$testAssembly" "/r:$sdk" "/r:$plugin" '/r:C:\Program Files\Rhino 8\Plug-ins\Grasshopper\GH_IO.dll' /r:System.Drawing.dll /r:System.Windows.Forms.dll "$root\tests\ToolLabelTests.cs"
if ($LASTEXITCODE -ne 0) { throw 'Tool label test compilation failed' }
foreach ($name in @('Eto.dll','RhinoCommon.dll')) { $null=[Reflection.Assembly]::LoadFrom("C:\Program Files\Rhino 8\System\$name") }
$null=[Reflection.Assembly]::LoadFrom('C:\Program Files\Rhino 8\Plug-ins\Grasshopper\GH_IO.dll')
$null=[Reflection.Assembly]::LoadFrom($sdk)
$null=[Reflection.Assembly]::LoadFrom($plugin)
$assembly=[Reflection.Assembly]::LoadFrom($testAssembly)
$result=$assembly.GetType('ToolLabelTests').GetMethod('Main',[Reflection.BindingFlags]'NonPublic,Static').Invoke($null,@())
if ($result -ne 0) { throw 'Tool label tests failed' }
