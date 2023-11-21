import {AGENT_OTP_ENVIRONMENT_VARIABLE} from './consts';

function getAgentDownloadCommand(ip, port, otp) {
  return `$execCmd = @"\r\n`
    + `\`$monkey=[System.IO.Path]::GetTempPath() + """monkey.exe""";\r\n`
    + `[Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12;\r\n`
    + `[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {\`$true};\r\n`
    + `(New-Object System.Net.WebClient).DownloadFile('https://${ip}:${port}/api/agent-binaries/windows',\r\n`
    + `"""\`$monkey""");\`$env:${AGENT_OTP_ENVIRONMENT_VARIABLE}='${otp}';\r\n`
    + `Start-Process -FilePath """\`$monkey""" -ArgumentList 'm0nk3y -s ${ip}:${port}';\r\n`
    + `"@; \r\n`
    + `Start-Process -FilePath powershell.exe -ArgumentList $execCmd`;
}

export default function generateLocalWindowsPowershell(ip, port, username, otp) {
  let command = getAgentDownloadCommand(ip, port, otp)
  if (username !== '') {
    command += ` -Credential ${username}`;
  }

  return command;
}
