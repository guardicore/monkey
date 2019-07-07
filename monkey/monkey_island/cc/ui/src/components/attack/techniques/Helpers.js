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
      machineStr += ipInfo['addr'] + " ";
    });
    return machineStr + ")"
}
