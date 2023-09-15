import {AGENT_OTP_ENVIRONMENT_VARIABLE} from './consts';

function getAgentDownloadCommand(ip, otp) {
  return `$execCmd = @"\r\n`
    + `\`$TempDir=[System.IO.Path]::GetTempPath();\r\n`
    + `read-host "press something"\r\n`
    + `[Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;\r\n`
    + `[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {\`$true};\r\n`
    + `(New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/agent-binaries/windows',\r\n`
    + `"\`$TempDir\\monkey.exe");\`$env:${AGENT_OTP_ENVIRONMENT_VARIABLE}='${otp}';\r\n`
    + `Start-Process -FilePath '\`$TempDir\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';\r\n`
    + `read-host "Press any key exit..."\r\n`
    + `"@; \r\n`
    + `Start-Process -FilePath powershell.exe -ArgumentList $execCmd`;
}

export default function generateLocalWindowsPowershell(ip, username, otp) {
  let command = getAgentDownloadCommand(ip, otp)
  if (username !== '') {
    command += ` -Credential ${username}`;
  }

  return command;
}
