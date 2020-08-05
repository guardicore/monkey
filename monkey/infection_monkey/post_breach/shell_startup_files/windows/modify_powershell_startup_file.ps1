param (
    [string]$startup_file_path = $profile
)


# check if paths exist already
$startup_file_prev_exists = Test-Path $startup_file_path
$startup_file_folder_path = ($startup_file_path -split '\\')[0..(($startup_file_path -split '\\').count -2)] -join '\'
$startup_file_folder_prev_exists = Test-Path $startup_file_folder_path

# carry out pba
If (!($startup_file_prev_exists)) {  # create profile.ps1 file if it doesn't exist already
    [Void](New-Item -Path $startup_file_path -ItemType "file" -Force)
}
Add-Content $startup_file_path "# Successfully modified $startup_file_path" ;  # add line to $Profile
cat $startup_file_path | Select -last 1 ;  # print last line of $Profile
$OldProfile = cat $startup_file_path | Select -skiplast 1 ;  # get file's original content
Set-Content $startup_file_path -Value $OldProfile ;  # restore file's original content

# cleanup
If (!($startup_file_prev_exists)) {  # remove file if it didn't exist previously
    Remove-Item -Path $startup_file_path -Force ;
}
If (!($startup_file_folder_prev_exists)) {  # remove folder if it didn't exist previously
    Remove-Item -Path $startup_file_folder_path -Force -Recurse ;
}
