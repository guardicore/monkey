function getAgentDownloadCommand(ip) {
  return `$execCmd = @"\r\n`
    + `[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {\`$true};`
    + `(New-Object System.Net.WebClient).DownloadFile('https://${ip}:5000/api/agent-binaries/windows',`
    + `"""$env:TEMP\\monkey.exe""");Start-Process -FilePath '$env:TEMP\\monkey.exe' -ArgumentList 'm0nk3y -s ${ip}:5000';`
    + `\r\n"@; \r\n`
    + `Start-Process -FilePath powershell.exe -ArgumentList $execCmd`;
}

export default function generateLocalWindowsPowershell(ip, username) {
  let command = getAgentDownloadCommand(ip)
  if (username !== '') {
    command += ` -Credential ${username}`;
  }

  return command;
}
