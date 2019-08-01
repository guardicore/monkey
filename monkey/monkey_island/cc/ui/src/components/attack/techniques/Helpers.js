import React from "react";

export function renderMachine(val){
    return (
      <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
    )
}

/* Function takes data gathered from system info collector and creates a
   string representation of machine from that data. */
export function renderMachineFromSystemData(data) {
    let machineStr = data['hostname'] + " ( ";
    data['ips'].forEach(function(ipInfo){
      if(typeof ipInfo === "object"){
        machineStr += ipInfo['addr'] + " ";
      } else {
         machineStr += ipInfo + " ";
      }
    });
    return machineStr + ")"
}

/* Formats telemetry data that contains _id.machine and _id.usage fields into columns
   for react table. */
export function getUsageColumns() {
    return ([{
      columns: [
        {Header: 'Machine',
          id: 'machine',
          accessor: x => renderMachineFromSystemData(x.machine),
          style: { 'whiteSpace': 'unset' },
          width: 300},
        {Header: 'Usage',
          id: 'usage',
          accessor: x => x.usage,
          style: { 'whiteSpace': 'unset' }}]
    }])}

export const ScanStatus = {
    UNSCANNED: 0,
    SCANNED: 1,
    USED: 2
};
