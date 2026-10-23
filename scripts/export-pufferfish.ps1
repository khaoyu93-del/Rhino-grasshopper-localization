$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$system = 'C:\Program Files\Rhino 8\System'
$ghRoot = 'C:\Program Files\Rhino 8\Plug-ins\Grasshopper'
foreach ($name in @('Eto.dll','RhinoCommon.dll')) { $null = [Reflection.Assembly]::LoadFrom("$system\$name") }
$null = [Reflection.Assembly]::LoadFrom("$ghRoot\GH_IO.dll")
$gh = [Reflection.Assembly]::LoadFrom("$ghRoot\Grasshopper.dll")
foreach ($name in @('XformComponents.gha','CurveComponents.gha','SurfaceComponents.gha','VectorComponents.gha','MathComponents.gha')) { $null = [Reflection.Assembly]::LoadFrom("$ghRoot\Components\$name") }
$path = Join-Path $env:APPDATA 'McNeel\Rhinoceros\packages\8.0\Pufferfish\3.0.0\Pufferfish3-0.gha'
$assembly = [Reflection.Assembly]::LoadFrom($path)
$opcodes = @{}
[Reflection.Emit.OpCodes].GetFields([Reflection.BindingFlags]'Public,Static') | ForEach-Object { $op = $_.GetValue($null); $opcodes[([int]$op.Value -band 65535)] = $op }
function Get-Strings($method) {
    $body = $method.GetMethodBody()
    if (!$body) { return }
    $bytes = $body.GetILAsByteArray()
    for ($i=0; $i -lt $bytes.Length;) {
        $code = [int]$bytes[$i++]
        if ($code -eq 254) { $code = 65024 + [int]$bytes[$i++] }
        $op = $opcodes[$code]
        $kind = $op.OperandType.ToString()
        $length = switch ($kind) {
            InlineNone {0} ShortInlineBrTarget {1} ShortInlineI {1} ShortInlineVar {1} InlineVar {2}
            InlineI {4} InlineBrTarget {4} InlineField {4} InlineMethod {4} InlineSig {4} InlineString {4} InlineTok {4} InlineType {4} ShortInlineR {4}
            InlineR {8} InlineI8 {8} InlineSwitch {4+4*[BitConverter]::ToInt32($bytes,$i)}
        }
        if ($kind -eq 'InlineString') { $method.Module.ResolveString([BitConverter]::ToInt32($bytes,$i)) }
        $i += $length
    }
}
function Get-PortDefinitions($method) {
    $bytes = $method.GetMethodBody().GetILAsByteArray()
    $strings = @()
    for ($i=0; $i -lt $bytes.Length;) {
        $code = [int]$bytes[$i++]
        if ($code -eq 254) { $code = 65024 + [int]$bytes[$i++] }
        $op = $opcodes[$code]
        $kind = $op.OperandType.ToString()
        $length = switch ($kind) {
            InlineNone {0} ShortInlineBrTarget {1} ShortInlineI {1} ShortInlineVar {1} InlineVar {2}
            InlineI {4} InlineBrTarget {4} InlineField {4} InlineMethod {4} InlineSig {4} InlineString {4} InlineTok {4} InlineType {4} ShortInlineR {4}
            InlineR {8} InlineI8 {8} InlineSwitch {4+4*[BitConverter]::ToInt32($bytes,$i)}
        }
        if ($kind -eq 'InlineString') { $strings += $method.Module.ResolveString([BitConverter]::ToInt32($bytes,$i)) }
        if ($kind -eq 'InlineMethod') {
            $called = $method.Module.ResolveMethod([BitConverter]::ToInt32($bytes,$i))
            if ($called.Name -match '^Add.+Parameter$|^AddParameter$' -and $strings.Count -ge 3) {
                @{name=$strings[0];nickname=$strings[1];description=($strings[2..($strings.Count-1)] -join '')}
                $strings = @()
            }
        }
        $i += $length
    }
}
$rows = @(); $texts = @(); $failures = @()
foreach ($type in $assembly.GetTypes() | Where-Object { !$_.IsAbstract -and $_.IsPublic -and $gh.GetType('Grasshopper.Kernel.IGH_DocumentObject').IsAssignableFrom($_) -and $_.GetConstructor([Type[]]@()) }) {
    $constructor = @(Get-Strings ($type.GetConstructor([Type[]]@())))
    try {
        $obj = [Activator]::CreateInstance($type)
        $inputs = @(); $outputs = @()
        if ($obj -is [Grasshopper.Kernel.IGH_Component]) {
            $inputs = @($obj.Params.Input | ForEach-Object { @{name=$_.Name; nickname=$_.NickName; description=$_.Description} })
            $outputs = @($obj.Params.Output | ForEach-Object { @{name=$_.Name; nickname=$_.NickName; description=$_.Description} })
        }
        $rows += @{guid=$obj.ComponentGuid.ToString();name=$obj.Name;nickname=$obj.NickName;description=$obj.Description;category=$obj.Category;subcategory=$obj.SubCategory;exposure=$obj.Exposure.ToString();type=$type.FullName;inputs=$inputs;outputs=$outputs;constructor=$constructor}
    } catch { $failures += @{type=$type.FullName;error=$_.Exception.GetBaseException().Message;constructor=$constructor} }
    foreach ($method in $type.GetMethods([Reflection.BindingFlags]'Instance,Static,Public,NonPublic,DeclaredOnly')) {
        $strings = @(Get-Strings $method)
        if ($strings.Count) {
            $ports = @()
            if ($method.Name -match '^Register.+Params$') { $ports = @(Get-PortDefinitions $method) }
            $texts += @{type=$type.FullName;method=$method.Name;strings=$strings;ports=$ports}
        }
    }
}
$users = @()
$userFolder = Join-Path (Split-Path $path -Parent) 'Pufferfish WIP SubD Components'
foreach ($file in Get-ChildItem -LiteralPath $userFolder -Filter '*.ghuser') {
    $user = New-Object Grasshopper.Kernel.GH_UserObject $file.FullName
    $user.ReadFromFile()
    $archive = New-Object GH_IO.Serialization.GH_Archive
    if (!$archive.Deserialize_Binary($user.Data)) { throw "Invalid user object: $($file.Name)" }
    $parameters = $archive.GetRootNode.Chunks | Where-Object Name -eq 'ParameterData'
    $inputs = @(); $outputs = @()
    foreach ($chunk in $parameters.Chunks) {
        if ($chunk.Name -notin @('InputParam','OutputParam')) { continue }
        $port = @{name=$chunk.GetString('Name');nickname=$chunk.GetString('NickName');description=$chunk.GetString('Description')}
        if ($chunk.Name -eq 'InputParam') { $inputs += $port } else { $outputs += $port }
    }
    $users += @{baseguid=$user.BaseGuid.ToString();name=$user.Description.Name;nickname=$user.Description.NickName;description=$user.Description.Description;category=$user.Description.Category;subcategory=$user.Description.SubCategory;inputs=$inputs;outputs=$outputs}
}
$output = Join-Path $root 'docs\pufferfish-catalog.json'
@{assembly=$assembly.GetName().Name;version=$assembly.GetName().Version.ToString();sdk=$gh.GetName().Version.ToString();tools=$rows;users=$users;failures=$failures;method_text=$texts} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $output -Encoding UTF8
"Pufferfish: components=$($rows.Count), failures=$($failures.Count), text methods=$($texts.Count)"
"Catalog: $output"
