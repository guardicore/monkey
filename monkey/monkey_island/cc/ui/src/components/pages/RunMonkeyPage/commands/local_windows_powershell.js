import {OS_TYPES} from '../utils/OsTypes';


export function getAgentDownloadCommand(ip, osType) {
  let bitText = osType === OS_TYPES.WINDOWS_32 ? '32' : '64';
  return `$execCmd = @"\r\n`
    + `-noexit [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {\`$true};`
    + `(New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/monkey/download/monkey-windows-${bitText}.exe',`
    + `"""$env:TEMP\\monkey.exe""");Start-Process -FilePath '$env:TEMP\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';`
    + `\r\n"@; \r\n`
    + `Start-Process -FilePath powershell.exe -ArgumentList $execCmd`
}

export default function generateLocalWindowsPowershell(ip, osType, username) {
  let command = getAgentDownloadCommand(ip, osType)
  if (username != '') {
    command += ` -Credential ${username}`;
  }

  return command;
}
