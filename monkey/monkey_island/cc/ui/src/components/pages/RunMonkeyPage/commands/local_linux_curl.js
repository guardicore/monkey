import {OS_TYPES} from '../OsTypes';


export default function generateLocalLinuxCurl(ip, osType) {
    let bitText = osType === OS_TYPES.LINUX_32 ? '32' : '64';
    return `curl https://${ip}:5000/api/monkey/download/monkey-linux-${bitText} -k
    -o monkey-linux-${bitText};
    chmod +x monkey-linux-${bitText};
    ./monkey-linux-${bitText} m0nk3y -s ${ip}:5000\`;`;
  }



