import {OS_TYPES} from '../utils/OsTypes';


export default function generateLocalWindowsPowershell(ip, osType, username) {
  let bitText = osType === OS_TYPES.WINDOWS_32 ? '32' : '64';
  let command = `[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}; `
    + `(New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/monkey/download/ `
    + `monkey-windows-${bitText}.exe','.\\monkey.exe'); `
    + `;Start-Process -FilePath '.\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';`;
  if (username != '')
      command = `Start-Process powershell.exe -ArgumentList "-noexit ${command}" -Credential ${username}`;
    return command;
}
