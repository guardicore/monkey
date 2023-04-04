const AGENT_OTP_ENVIRONMENT_VARIABLE = 'MONKEY_OTP'

function getAgentDownloadCommand(ip, otp) {
  return `$execCmd = @"\r\n`
    + `[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {\`$true};`
    + `(New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/agent-binaries/windows',`
    + `"""$env:TEMP\\monkey.exe""");\`$env:${AGENT_OTP_ENVIRONMENT_VARIABLE}='${otp}' ;`
    + `Start-Process -FilePath '$env:TEMP\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';`
    + `\r\n"@; \r\n`
    + `Start-Process -FilePath powershell.exe -ArgumentList $execCmd`;
}

export default function generateLocalWindowsPowershell(ip, username, otp) {
  let command = getAgentDownloadCommand(ip, otp)
  if (username !== '') {
    command += ` -Credential ${username}`;
  }

  return command;
}
