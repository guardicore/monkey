import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';



export function doesAnyAgentExist() {
  return getAllAgents().then(all_agents => {
    if (all_agents.length > 0) {return true;}
    return false;
    })
}

export function didAllAgentsShutdown() {
  return getAllAgents().then(all_agents => {
    for (let idx in all_agents) {
      let agent = all_agents[idx];
      if (agent.stop_time === null) {return false;}
    }
    return true;
  })
}

export function getCollectionObject(collectionEndpoint: APIEndpoint, key: string) {
  return IslandHttpClient.get(collectionEndpoint)
      .then(res => {
        return arrayToObject(res.body, key);
      })
}

export function arrayToObject(array: object[], key: string): Record<string, any>{
  return array.reduce((prev, curr) => ({...prev, [curr[key]]: curr}), {});
}

export function getAllAgents() {
    return IslandHttpClient.get(APIEndpoint.agents)
    .then(res => {
        return res.body;
    });
}

export function getMachineHostnname(machine): string {
  let hostname = "unknown";

  if ((machine['hostname'] !== null) && (machine['hostname'] !== '')) {
    hostname = machine['hostname'];
  }
  else {
    hostname = machine['network_interfaces'][0].split('/')[0];
  }

  return hostname;
}

export function getEventSourceHostname(event_source, agents, machines): string {
  let hostname = "unknown";

  for (let agent of agents) {
    if (event_source === agent['id']) {
      for (let machine of machines) {
        if (agent['machine_id'] === machine['id']) {
          hostname = getMachineHostnname(machine)
          break;
        }
      }
      break;
    }
  }

  return hostname;
}
