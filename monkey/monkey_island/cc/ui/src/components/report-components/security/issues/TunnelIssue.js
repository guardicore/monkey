import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';
import {getMachineByAgent, getMachineFromIP, getMachineHostname, getMachineIPs} from '../../../utils/ServerUtils';


export function getAllTunnels(agents, machines) {
  let islandIPs = [];
  for (let machine of machines) {
    if (machine.island === true) {
      islandIPs = islandIPs.concat(
        ...getMachineIPs(machine)
      );
    }
  }

  let tunnels = [];
  for (let agent of agents) {
    if (!islandIPs.includes(agent.cc_server.ip)) {
      let agentMachine = getMachineByAgent(agent, machines);
      if (agentMachine !== null) {
        let agentMachineHostname = getMachineHostname(agentMachine)

        let agentTunnelMachineHostname = agent.cc_server.ip;
        let agentTunnelMachine = getMachineFromIP(agent.cc_server.ip, machines)
        if (agentTunnelMachine !== null) {
          agentTunnelMachineHostname = getMachineHostname(agentTunnelMachine);
        }

        tunnels.push({
          'agent_machine': agentMachineHostname,
          'agent_tunnel': agentTunnelMachineHostname
        });
      }
    }
  }
  return tunnels;
}

export function tunnelIssueOverview(allTunnels) {
  if (allTunnels.length > 0) {
    return ( <li key="tunnel">Weak segmentation -
      Machines were able to relay communications over unused ports.</li>)
  } else {
    return null;
  }
}

export function tunnelIssueReportByMachine(machine, allTunnels) {
  if (allTunnels.length > 0) {
    let tunnelIssuesByMachine = getTunnelIssuesByMachine(machine, allTunnels);

    if (tunnelIssuesByMachine.length > 0) {
      return (
        <>
          Use micro-segmentation policies to disable communication other than the required.
          <CollapsibleWellComponent>
            Machines are not locked down at port level.
            Network tunnels were set up between the following.
            <ul>
              {tunnelIssuesByMachine}
            </ul>
          </CollapsibleWellComponent>
        </>
      );
    }
  }

  return null;
}

function getTunnelIssuesByMachine(machine, allTunnels) {
  let tunnelIssues = [];

  for (let tunnel of allTunnels) {
    // TODO: After #2569, the values in `tunnel` can also be hostnames and not only IP addresses.
    //       Check what values `machine` can be and modify this check if required.
    //       `tunnel` looks like `{"agent_machine": <IP/hostname>, "agent_tunnel": <IP/hostname>}`.
    if (Object.values(tunnel).includes(machine)) {
      tunnelIssues.push(
        <li key={tunnel.agent_machine+tunnel.agent_tunnel}>
          from <span className="badge badge-primary">{tunnel.agent_machine}
          </span> to <span className="badge badge-primary">{tunnel.agent_tunnel}</span>
        </li>
      );
    }
  }

  return tunnelIssues;
}
