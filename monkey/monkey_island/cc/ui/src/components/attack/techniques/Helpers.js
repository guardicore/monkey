import React from 'react';

export function renderMachine(val) {
  return (
    <span>{val.ip_addr} {(val.domain_name ? ' ('.concat(val.domain_name, ')') : '')}</span>
  )
}

/* Function takes data gathered from system info collector and creates a
   string representation of machine from that data. */
export function renderMachineFromSystemData(data) {
  let machineStr = '';
  if (typeof data['hostname'] !== 'undefined') {
    machineStr = data['hostname'] + ' ( ';
  }
  data['ips'].forEach(function (ipInfo) {
    if (typeof ipInfo === 'object') {
      machineStr += ipInfo['addr'] + ', ';
    } else {
      machineStr += ipInfo + ', ';
    }
  });
  if (typeof data['hostname'] !== 'undefined') {
    return machineStr.slice(0, -2) + ' )';
  } else {
    // Replaces " ," with " )" to finish a list of IP's
    return machineStr.slice(0, -2);
  }
}

/* Formats telemetry data that contains _id.machine and _id.usage fields into columns
   for react table. */
export function getUsageColumns() {
  return ([{
    columns: [
      {
        Header: 'Machine',
        id: 'machine',
        accessor: x => renderMachineFromSystemData(x.machine),
        style: {'whiteSpace': 'unset'},
        width: 300
      },
      {
        Header: 'Usage',
        id: 'usage',
        accessor: x => x.usage,
        style: {'whiteSpace': 'unset'}
      }]
  }])
}

/* Renders table fields that contains 'used' boolean value and 'name' string value.
'Used' value determines if 'name' value will be shown.
 */
export function renderUsageFields(usages) {
  let output = [];
  usages.forEach(function (usage) {
    if (usage['used']) {
      output.push(<div key={usage['name']}>{usage['name']}</div>)
    }
  });
  return (<div>{output}</div>);
}

export const ScanStatus = {
  UNSCANNED: 0,
  SCANNED: 1,
  USED: 2,
  DISABLED: 3
};
