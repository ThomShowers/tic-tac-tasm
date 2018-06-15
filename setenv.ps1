##
# Sets up a build environment for Windows (include/lib, path, cl.exe, etc.)
#
# Use the following command to run the script in the context of your shell:
#
#   Invoke-Expression ((Get-Content .\setenv.ps1) -Join "`r`n")
#
##

function Use-BuildEnv {
    param([string]$hostArch, [string]$arch)

    if ($hostArch) {
        $hostArch = "-host_arch=$hostArch"
    }

    if ($arch) {
        $arch = "-arch=$arch"
    }

    $vslocation = Get-VsLocation

    cmd /s /c """$vslocation\Common7\Tools\vsdevcmd.bat""  $hostArch $arch && set" | Where-Object { 
        $_ -match '(\w+)=(.*)' 
    } | ForEach-Object { 
        Invoke-Expression "`$env:$($matches[1]) = `"$($matches[2])`""
    }

    $env:Path += ";$clPath"
}

function Get-VsLocation {

    $vswhere = "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
    if (!(Test-Path -Path $vswhere -PathType Leaf)) {
        $vswhere = $null
    }

    if (!$vswhere) {
        Write-Host "searching for vswhere.exe..."
        $vswhere = @(where.exe vswhere.exe 2> $null)[0]
    }

    if (!$vswhere) {
        $systemDrive = $env:SystemDrive
        if ($systemDrive) {
            $vswhere = @(where.exe /r $systemDrive\ vswhere.exe 2> $null)[0]
        }
    }

    if (!$vswhere) {
        Get-PSDrive | Where-Object { 
            $_.Provider -eq "FileSystem" -and $_.Root -ne "$systemDrive\" 
        } | ForEach-Object {
            if (!$vswhere) {
                $vswhere = @(where.exe /r $_.Root vswhere.exe 2> $null)[0]
            }
        }
    }

    if ($vswhere -eq $null) {
        Write-Error "Failed to locate vswhere.exe"
        exit 1
    }

    & $vswhere -latest -property installationPath -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64
}

Use-BuildEnv amd64 x86
