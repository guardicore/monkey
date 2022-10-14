import IslandHttpClient from '../IslandHttpClient';

export function doesAnyAgentExist() {
  return _getAllAgents().then(all_agents => {
    if (all_agents.length > 0) {return true;}
    return false;
    })
}

export function didAllAgentsShutdown() {
  return _getAllAgents().then(all_agents => {
    for (let idx in all_agents) {
      let agent = all_agents[idx];
      if (agent.stop_time === null) {return false;}
    }
    return true;
  })
}

function _getAllAgents() {
    return IslandHttpClient.get('/api/agents')
    .then(res => {
        return res.body;
    });
}
