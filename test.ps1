Get-ChildItem -Path "$PSScriptRoot/tests/unittests" -Recurse -Include *_tests.py | ForEach-Object {
    python $_.FullName
}