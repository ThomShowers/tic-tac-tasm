Get-ChildItem -Path "$PSScriptRoot/tests" -Recurse -Include *_tests.py | ForEach-Object {
    python $_.FullName
}