const AGENT_OTP_ENVIRONMENT_VARIABLE = 'MONKEY_OTP'

export default function generateLocalLinuxWget(ip, username, otp) {
  let command = `wget --no-check-certificate https://${ip}:5000/api/agent-binaries/`
    + `linux -O ./monkey-linux-64; `
    + `chmod +x monkey-linux-64; `
    + `${AGENT_OTP_ENVIRONMENT_VARIABLE}=${otp} ./monkey-linux-64 m0nk3y -s ${ip}:5000`;

  if (username != '') {
    command = `su - ${username} -c "${command}"`;
  }

  return command;
}
