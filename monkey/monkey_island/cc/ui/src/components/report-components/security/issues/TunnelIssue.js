import React from 'react';
import CollapsibleWellComponent from '../CollapsibleWell';
import {getMachineByAgent, getMachineFromIP, getMachineHostname, getMachineIPs} from '../../../utils/ServerUtils';

export function tunnelIssueOverview(agents, machines) {
  if(getTunnels(agents, machines).length > 0){
    return ( <li key="tunnel">Weak segmentation -
      Machines were able to relay communications over unused ports.</li>)
  } else {
    return null;
  }
}

export function tunnelIssueReport(agents, machines) {
  let tunnels = getTunnels(agents, machines);

  if(tunnels.length > 0){
    return (
      <>
        Use micro-segmentation policies to disable communication other than the required.
        <CollapsibleWellComponent>
          Machines are not locked down at port level.
          Network tunnels were set up between the following.
          <ul>
            {tunnels.map(tunnel =>
              <li>
                from <span className="badge badge-primary">{tunnel.agent_machine}
                </span> to <span className="badge badge-primary">{tunnel.agent_tunnel}</span>
              </li>
            )}
          </ul>
        </CollapsibleWellComponent>
      </>
    );
  } else {
    return null;
  }
}

function getTunnels(agents, machines) {
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
