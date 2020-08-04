param (
    [string]$startup_file_path = $profile
)

If (!(Test-Path $startup_file_path)) {  # create profile.ps1 file if it doesn't exist already
    New-Item -Path $startup_file_path -ItemType "file" -Force
}
Add-Content $startup_file_path "# Successfully modified $startup_file_path" ;  # add line to $Profile
cat $startup_file_path | Select -last 1 ;  # print last line of $Profile
$OldProfile = cat $startup_file_path | Select -skiplast 1 ;
Set-Content $startup_file_path -Value $OldProfile ;
