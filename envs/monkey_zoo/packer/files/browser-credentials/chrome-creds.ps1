<#
  Made with <3 by Marco Simioni <marcosim@ie.ibm.com>

  This script can be used to list all credentials found in the Chrome Local Store.
  It can also be used to Export and Import credentials one by one, with the ability to customize them:
  the script will in fact take care of decrypting/re-encrypting passwords as per [1] and [2].

  Tested on Windows 10 Enterprise, Version 20H2, OS Build 19042.1466, and Chrome Version 97.0.4692.71 (Official Build) (64-bit).

  History:

  **13-Jan-2022 v.1.0.0**: add capability to extract and re-import credentials into the store.
  **04-Feb-2022 v.1.0.1**: add ability to specify LocalAppData path via param.
  **08-Feb-2022 v.1.0.2**: add command to delete all credentials.

  [1] https://xenarmor.com/how-to-recover-saved-passwords-google-chrome/
  [2] https://jhoneill.github.io/powershell/2020/11/23/Chrome-Passwords.html
	>

<# Based on https://www.powershellgallery.com/packages/Read-Chromium/1.0.0/Content/Read-Chromium.ps1
   Copyright James O'Neill 2020.
   Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"),
   to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
   and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
   The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
   WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
   #>


param (
	$LocalAppDataPath = (Get-ChildItem Env:\LOCALAPPDATA).Value,
	$LoginDataPath = "$LocalAppDataPath\Google\Chrome\User Data\Default\Login Data",
	$LocalStatePath = "$LocalAppDataPath\Google\Chrome\User Data\Local State",

	$Command = "List", # Can be List, Export, or Import

	$id = -1,

	$origin_url = 'https://demo.testfire.net/login.jsp',
	$action_url = 'https://demo.testfire.net/doLogin',
	$username_element = 'uid',
	$username_value = 'jsmith',
	$password_element = 'passw',
	$password_value = 0000000000,
	$submit_element = '',
	$signon_realm = 'https://demo.testfire.net/',
	$blacklisted_by_user = '0',
	$scheme = '0',
	$password_type = '0',
	$times_used = '0',
	$form_data = '3401000007000000050000006c006f00670069006e0000002300000068747470733a2f2f64656d6f2e74657374666972652e6e65742f6c6f67696e2e6a7370002100000068747470733a2f2f64656d6f2e74657374666972652e6e65742f646f4c6f67696e00000002000000090000000000000003000000750069006400000000000000040000007465787400000000ffffff7f00000000000000000000000001000000010000000100000002000000000000000000000000000000050000000000000000000000090000000000000005000000700061007300730077000000000000000800000070617373776f726400000000ffffff7f0000000000000000000000000100000001000000010000000200000000000000000000000000000005000000000000000000000001000000040000006e756c6c',
	$display_name = '',
	$icon_url = '',
	$federation_url = '',
	$skip_zero_click = '0',
	$generation_upload_status = '0',
	$possible_username_pairs = '00000000',
	$moving_blocked_for = '00000000'
)

function HexToByteArray([string]$hex) {(0..([Math]::Floor( ($hex.Length+1)/2)-1)).ForEach({[Convert]::ToByte($(if ($hex.Length -ge 2*($_+1)) {$hex.Substring($_*2,2)} else {$hex.Substring($_*2,1).PadRight(2,'0')}),16)})}

$scriptVersion = "1.0.2"
$scriptName = $MyInvocation.MyCommand.Name
$scriptPath = (Get-Item .).FullName

Write-Host
Write-Host "chrome-creds ${scriptVersion} made with <3 by Marco Simioni <marcosim@ie.ibm.com>"
Write-Host

Write-Host "LocalAppDataPath: $LocalAppDataPath"
Write-Host "LoginDataPath: $LoginDataPath"
Write-Host "LocalStatePath: $LocalStatePath"
Write-Host

Add-Type -AssemblyName System.Security
$bouncyccastledll = ".\BouncyCastle.Crypto.dll"

# Unblock and load BouncyCastle.Crypto.dll
Unblock-File $bouncyccastledll
Add-Type -Path $bouncyccastledll

# Get the master key and use it to create a AesGCcm object for decoding
if ($LocalStatePath) {$localStateInfo = Get-Content -Raw $LocalStatePath | ConvertFrom-Json}
if ($localStateInfo) {$encryptedkey   = [convert]::FromBase64String($localStateInfo.os_crypt.encrypted_key)}
if ($encryptedkey -and [string]::new($encryptedkey[0..4]) -eq 'DPAPI') {
    $masterKey       = [System.Security.Cryptography.ProtectedData]::Unprotect(($encryptedkey | Select-Object -Skip 5),  $null, 'CurrentUser')
    $Script:GCMKey   = $masterKey
}
else {Write-Warning  'Could not get key for new-style encyption. Will try with older Style' }

function GcmEncrypt {
    Param ( [byte[]]$nonce, [byte[]]$plainTextData, [ref]$output, [ref]$tag, [byte[]]$key, [byte[]]$associatedText )

    $cipher = [Org.BouncyCastle.Crypto.Engines.AesEngine]::new();
    $macSize = 8*$cipher.GetBlockSize();
    $keyParam = [Org.BouncyCastle.Crypto.Parameters.KeyParameter]::new($key);
    $keyParamAead = [Org.BouncyCastle.Crypto.Parameters.AeadParameters]::new($keyParam, $macSize, $nonce, $associatedText);
    $cipherMode = [Org.BouncyCastle.Crypto.Modes.GcmBlockCipher]::new($cipher);
    $cipherMode.Init($true, $keyParamAead);
    $outputSize = $cipherMode.GetOutputSize($plainTextData.Length);
    $cipherTextData = [byte[]]::new($outputSize);
    $result = $cipherMode.ProcessBytes($plainTextData, 0, $plainTextData.Length, $cipherTextData, 0);
    $result = $cipherMode.DoFinal($cipherTextData, $result);
    $output.Value = $cipherTextData[0..($plainTextData.Length - 1)]
    $tag.Value = $cipherTextData[$plainTextData.Length..($cipherTextData.Length - 1)]
}

function GcmDecrypt {
    Param ( [byte[]]$nonce, [byte[]]$cipherTextData, [byte[]]$tag, [ref]$output, [byte[]]$key, [byte[]]$associatedText )

    $fullCipherData = $cipherTextData + $tag
    $cipher = [Org.BouncyCastle.Crypto.Engines.AesEngine]::new();
    $macSize = 8*$cipher.GetBlockSize();
    $keyParam = [Org.BouncyCastle.Crypto.Parameters.KeyParameter]::new($key);
    $keyParamAead = [Org.BouncyCastle.Crypto.Parameters.AeadParameters]::new($keyParam, $macSize, $nonce, $associatedText);
    $cipherMode = [Org.BouncyCastle.Crypto.Modes.GcmBlockCipher]::new($cipher);
    $cipherMode.Init($false, $keyParamAead);
    $result = $cipherMode.ProcessBytes($fullCipherData, 0, $fullCipherData.Length, $output.Value, 0);
    $result = $cipherMode.DoFinal($output.Value, $result);
}

# Used to decrypt passwords
# Use AES GCM decryption if ciphertext starts "V10" & GCMKey exists, else try ProtectedData.unprotect
# (See https://xenarmor.com/how-to-recover-saved-passwords-google-chrome/)
function DecryptPassword  {
    Param ( $Encrypted )

    try {
        if ($Script:GCMKey -and [string]::new($Encrypted[0..2]) -match "v1\d") {
            #Ciphertext bytes run 0-2="V10"; 3-14=12_byte_IV; 15 to len-17=payload; final-16=16_byte_auth_tag
            [byte[]]$output =  1..($Encrypted.length - 31) # same length as payload.
			$iv = $Encrypted[3..14]
			$cipherText = $Encrypted[15..($Encrypted.Length-17)]
			$tag = $Encrypted[-16..-1]
            GcmDecrypt -nonce $iv -cipherTextData $cipherText -tag $tag -output:([ref]$output) -key $Script:GCMKey -associatedText $null
            [string]::new($output)
        }
        else {[string]::new([System.Security.Cryptography.ProtectedData]::Unprotect($Encrypted,  $null, 'CurrentUser')) }
    }
    catch {Write-Warning "Error decrypting password ${Encrypted}: $_"}
}

function StrOrEmpty {
    Param ( $Strval )

    if ([string]::IsNullOrEmpty($Strval)) {
        return ""
    }
    return $Strval
}


# Used to encrypt passwords
# Uses AES GCM encryption if GCMKey exists, otherwise ProtectedData.Protect
function EncryptPassword  {
    Param ( $Unencrypted )

    try {
        if ($Script:GCMKey) {
			$iv = New-Object byte[] 12
			# Generate the empty byte arrays which will be filled with data during encryption
			$tag = [byte[]]::new(16)
			$output = [byte[]]::new($Unencrypted.Length) # same length as payload.
            [byte[]] $passwordData = [system.Text.Encoding]::UTF8.GetBytes($Unencrypted)
            GcmEncrypt -nonce $iv -plainTextData $passwordData -output:([ref]$output) -tag:([ref]$tag) -key $Script:GCMKey -associatedText $null
			$ver = [system.Text.Encoding]::UTF8.GetBytes("v10")
            #Ciphertext bytes run 0-2="V10"; 3-14=12_byte_IV; 15 to len-17=payload; final-16=16_byte_auth_tag
			[byte[]] $protected = $ver + $iv + $output + $tag
			return ,$protected # This is needed to return a byte array, see https://stackoverflow.com/a/61440166/2018733
        }
        else {[string]::new([System.Security.Cryptography.ProtectedData]::Protect($Unencrypted, $null, 'CurrentUser')) }
    }
    catch {
		Write-Warning "Error encrypting password ${Unencrypted}"
		Write-Warning $_
	}
}

# Test if System.Data.SQLite.dll is available
$sqlitedll = ".\System.Data.SQLite.dll"

if (!(Test-Path -Path $sqlitedll))
{
    Write-Host "Your bitness is:" (8*[IntPtr]::Size) -ForegroundColor Yellow
    Write-Host "Your .Net version is:" ([System.Runtime.InteropServices.RuntimeEnvironment]::GetSystemVersion()) -ForegroundColor Yellow
	Write-Host
    Write-Host "This script needs ""System.Data.SQLite.dll"" to be present in the current directory. Please follow these steps:" -ForegroundColor Yellow
	Write-Host
	Write-Host "- Download the SQLite static binary bundle from http://system.data.sqlite.org/index.html/doc/trunk/www/downloads.wiki." -ForegroundColor Yellow
	if ([intptr]::Size -eq 8)
	{
		Write-Host "  (You most likely need: http://system.data.sqlite.org/downloads/1.0.115.5/sqlite-netFx40-static-binary-bundle-x64-2010-1.0.115.5.zip)" -ForegroundColor Yellow
	} else {
		Write-Host "  (You most likely need: http://system.data.sqlite.org/downloads/1.0.115.5/sqlite-netFx40-static-binary-bundle-Win32-2010-1.0.115.5.zip)" -ForegroundColor Yellow
	}
	Write-Host "- Extract ""System.Data.SQLite.dll"" from the downloaded archive, and put it in the current directory (""${scriptPath}"")." -ForegroundColor Yellow
	Write-Host "- Re-run this script." -ForegroundColor Yellow
    return
}

# Unblock and load System.Data.SQLite.dll
Unblock-File $sqlitedll
Add-Type -Path $sqlitedll


# Open the SQLite database
$conn = New-Object -TypeName System.Data.SQLite.SQLiteConnection
$conn.ConnectionString = ("Data Source="""+$LoginDataPath+""";Default Timeout=5")
$conn.Open()

# Check if database is locked
Write-Host "Opening ${LoginDataPath}..."
try {
	$sql = "SELECT 0 from logins"
	$cmd = $conn.CreateCommand()
	$cmd.CommandText = $sql
	$res = $cmd.ExecuteNonQuery()
} catch {
	Write-Warning "Cannot read from the SQLite database ""${LoginDataPath}"": most likely it is locked. Please close your Chrome browser and retry." ; return
	}

# Execute the requested command
Switch ($Command)
{
		"List" {
			Write-Host "Listing all credentials stored..."

			$sql = "SELECT * FROM logins"
			$cmd = $conn.CreateCommand()
			$cmd.CommandText = $sql
			$adapter = New-Object -TypeName System.Data.SQLite.SQLiteDataAdapter $cmd
			$data = New-Object System.Data.DataSet
			$res = $adapter.Fill($data)

			$arrExp=@()
			foreach ($datarow in $data.Tables.rows)
			{
				Write-Host "Decoding" $datarow.origin_url "..."
				$row = New-Object psobject
				$row | Add-Member -Name id -MemberType NoteProperty -Value ($datarow.id)
				$row | Add-Member -Name URL -MemberType NoteProperty -Value ($datarow.origin_url)
				$row | Add-Member -Name UserName -MemberType NoteProperty -Value ($datarow.username_value)
				$row | Add-Member -Name Password -MemberType NoteProperty -Value ((DecryptPassword $datarow.password_value))
				$arrExp += $row
			}

			$cmd.Dispose()

			# Let's display the result
			if (Test-Path Variable:PSise)
			{
				$arrExp | Out-GridView
			}
			else
			{
				$arrExp | Format-Table
			}

			Write-Host "You can now chose an ID from the list, and export credentials as an executable import command with:"
			Write-Host
			Write-Host "./$scriptName -command Export -id <id>"
		}

		"Export" {

			if ($id -lt 0) {
				Write-Warning "You need to indicate the credentials to be exported, by specifying the parameter -id  as follows:"
				Write-Warning "./$scriptName -command Export -id 1"
				return
			}

			Write-Host "Exporting credential with id" $id "..."

			$sql = "SELECT * FROM logins WHERE id=@id"
			$cmd = $conn.CreateCommand()
			$cmd.CommandText = $sql
			$param = $cmd.Parameters.AddWithValue("@id", $id)
			$adapter = New-Object -TypeName System.Data.SQLite.SQLiteDataAdapter $cmd
			$data = New-Object System.Data.DataSet
			$res = $adapter.Fill($data)

			$arrExp=@()
			foreach ($datarow in $data.Tables.rows)
			{
				Write-Host "Exporting creds for" $datarow.origin_url "..."

				$exp = "./$scriptName -Command Import ```n"
				$exp += "	-origin_url " + (StrOrEmpty($datarow.origin_url)) + " ```n"
				$exp += "	-action_url " + (StrOrEmpty($datarow.action_url)) + " ```n"
				$exp += "	-username_element " + (StrOrEmpty($datarow.username_element)) + " ```n"
				$exp += "	-username_value " + (StrOrEmpty($datarow.username_value)) + " ```n"
				$exp += "	-password_element " + (StrOrEmpty($datarow.password_element)) + " ```n"
				$exp += "	-password_value " + (DecryptPassword $datarow.password_value) + " ```n"
				$exp += "	-submit_element " + (StrOrEmpty($datarow.submit_element)) + " ```n"
				$exp += "	-signon_realm " + (StrOrEmpty($datarow.signon_realm)) + " ```n"
				$exp += "	-blacklisted_by_user " + $datarow.blacklisted_by_user + " ```n"
				$exp += "	-scheme " + $datarow.scheme + " ```n"
				$exp += "	-password_type " + $datarow.password_type + " ```n"
				$exp += "	-times_used " + $datarow.times_used + " ```n"
				$exp += "	-form_data " + [BitConverter]::ToString($datarow.form_data) + " ```n"
				$exp += "	-display_name " + (StrOrEmpty($datarow.display_name)) + " ```n"
				$exp += "	-icon_url " + (StrOrEmpty($datarow.icon_url)) + " ```n"
				$exp += "	-federation_url " + (StrOrEmpty($datarow.federation_url)) + " ```n"
				$exp += "	-skip_zero_click " + $datarow.skip_zero_click + " ```n"
				$exp += "	-generation_upload_status " + $datarow.generation_upload_status + " ```n"
				$exp += "	-possible_username_pairs " + [BitConverter]::ToString($datarow.possible_username_pairs) + " ```n"
				$exp += "	-moving_blocked_for " + [BitConverter]::ToString($datarow.moving_blocked_for) + " `n"

				Write-Host
				Write-Host $exp
				Write-Host
				Write-Host "...exported! Just copy and paste the above command for inserting or updating the chosen creds into the store."
				Write-Host "(Remember you can customize username_value and password_value, or any other parameter for that matter)."
			}

			$cmd.Dispose()
		}

		"Import" {
			Write-Host "Importing..."

			$cmd = $conn.CreateCommand()

			$sql = "INSERT OR REPLACE INTO main.logins (origin_url, action_url, username_element, username_value, password_element, password_value, submit_element, signon_realm, date_created, blacklisted_by_user, scheme, password_type, times_used, form_data, display_name, icon_url, federation_url, skip_zero_click, generation_upload_status, possible_username_pairs, date_last_used, moving_blocked_for, date_password_modified)"
			$sql += " VALUES (@origin_url, @action_url, @username_element, @username_value, @password_element, @password_value, @submit_element, @signon_realm, @date_created, @blacklisted_by_user, @scheme, @password_type, @times_used, @form_data, @display_name, @icon_url, @federation_url, @skip_zero_click, @generation_upload_status, @possible_username_pairs, @date_last_used, @moving_blocked_for, @date_password_modified);"

			$password_value = EncryptPassword $password_value

			$param = $cmd.Parameters.AddWithValue("@origin_url", $origin_url)
			$param = $cmd.Parameters.AddWithValue("@action_url", $action_url)
			$param = $cmd.Parameters.AddWithValue("@username_element", $username_element)
			$param = $cmd.Parameters.AddWithValue("@username_value", $username_value)
			$param = $cmd.Parameters.AddWithValue("@password_element", $password_element)
			$param = $cmd.Parameters.AddWithValue("@password_value", $password_value)
			$param = $cmd.Parameters.AddWithValue("@submit_element", $submit_element)
			$param = $cmd.Parameters.AddWithValue("@signon_realm", $signon_realm)
			$param = $cmd.Parameters.AddWithValue("@date_created", ([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() * 1000))
			$param = $cmd.Parameters.AddWithValue("@blacklisted_by_user", $blacklisted_by_user)
			$param = $cmd.Parameters.AddWithValue("@scheme", $scheme)
			$param = $cmd.Parameters.AddWithValue("@password_type", $password_type)
			$param = $cmd.Parameters.AddWithValue("@times_used", $times_userd)
			$param = $cmd.Parameters.AddWithValue("@form_data", (HexToByteArray($form_data)))
			$param = $cmd.Parameters.AddWithValue("@display_name", $display_name)
			$param = $cmd.Parameters.AddWithValue("@icon_url", $icon_url)
			$param = $cmd.Parameters.AddWithValue("@federation_url", $federation_url)
			$param = $cmd.Parameters.AddWithValue("@skip_zero_click", $skip_zero_click)
			$param = $cmd.Parameters.AddWithValue("@generation_upload_status", $generation_upload_status)
			$param = $cmd.Parameters.AddWithValue("@possible_username_pairs", (HexToByteArray($possible_username_pairs)))
			#$param = $cmd.Parameters.AddWithValue("@id", '9') # AUTO INCREMENT
			$param = $cmd.Parameters.AddWithValue("@date_last_used",  ([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() * 1000))
			$param = $cmd.Parameters.AddWithValue("@moving_blocked_for", (HexToByteArray($moving_blocked_for)))

			$param = $cmd.Parameters.AddWithValue("@date_password_modified", ([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds() * 1000))

			$cmd.CommandText = $sql
			$res = $cmd.ExecuteNonQuery()

			$cmd.dispose()

			Write-Host "...credential imported!"

		}

		"Delete" {
			Write-Host "Deleting all credentials..."

			$cmd = $conn.CreateCommand()

			$sql = "DELETE FROM main.logins"
			$cmd.CommandText = $sql
			$res = $cmd.ExecuteNonQuery()

			$cmd.dispose()

			Write-Host "...all credentials deleted!"

		}
}

#$conn.Close()
