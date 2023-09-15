import {AGENT_OTP_ENVIRONMENT_VARIABLE} from './consts';

function getAgentDownloadCommand(ip, otp) {
  return `$execCmd =  [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes({\r\n`
  + `$monkey=[System.IO.Path]::GetTempPath() + "monkey.exe"\r\n`
  + `[Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;\r\n`
  + `[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true};\r\n`
  + `(New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/agent-binaries/windows',\r\n`
  + `"$monkey"); $env:${AGENT_OTP_ENVIRONMENT_VARIABLE}='${otp}';\r\n`
  + `Start-Process -FilePath "$monkey" -ArgumentList 'm0nk3y -s ${ip}:5000';\r\n`
  + `}))\r\n`
  + `Start-Process powershell -args '-EncodedCommand',$execCmd`;
}

export default function generateLocalWindowsPowershell(ip, username, otp) {
  let command = getAgentDownloadCommand(ip, otp)
  if (username !== '') {
    command += ` -Credential ${username}`;
  }

  return command;
}
