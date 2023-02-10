export default function generateLocalLinuxCurl(ip, username) {
  let command = `curl https://${ip}:5000/api/agent-binaries/linux -k `
    + `-o monkey-linux-64; `
    + `chmod +x monkey-linux-64; `
    + `./monkey-linux-64 m0nk3y -s ${ip}:5000;`;

  if (username != '') {
    command = `su - ${username} -c "${command}"`;
  }

  return command;
}
