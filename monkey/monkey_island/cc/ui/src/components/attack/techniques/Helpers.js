import React from "react";

export function RenderMachine(val){
    return (
      <span>{val.ip_addr} {(val.domain_name ? " (".concat(val.domain_name, ")") : "")}</span>
    )
}

export function renderMachineFromSystemData(data) {
    let machineStr = data['hostname'] + " ( ";
    data['ips'].forEach(function(ipInfo){
      machineStr += ipInfo['addr'] + " ";
    });
    return machineStr + ")"
}
