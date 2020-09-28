import {OS_TYPES} from '../OsTypes';


export default function generateLocalWindowsCmd(ip, osType) {
  let bitText = osType === OS_TYPES.WINDOWS_32 ? '32' : '64';
  return `powershell [System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true};
   (New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/monkey/download/
   monkey-windows-${bitText}.exe','.\\monkey.exe');
   ;Start-Process -FilePath '.\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';`;
}
