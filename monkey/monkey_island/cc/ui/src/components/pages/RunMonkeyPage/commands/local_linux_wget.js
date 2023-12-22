import { AGENT_OTP_ENVIRONMENT_VARIABLE } from './consts';

export default function generateLocalLinuxWget(ip, port, username, otp) {
  let command = `wget --no-check-certificate https://${ip}:${port}/api/agent-binaries/`
    + `linux -O ./monkey-linux-64; `
    + `chmod +x monkey-linux-64; `
    + `${AGENT_OTP_ENVIRONMENT_VARIABLE}=${otp} ./monkey-linux-64 m0nk3y -s ${ip}:${port}`;

  if (username != '') {
    command = `su - ${username} -c "${command}"`;
  }

  return command;
}
