import IslandHttpClient from '../IslandHttpClient';

export function doesAnyAgentExist() {
    let any_agent_exists = false;
    let all_agents = _getAllAgents();
    if (all_agents.length > 0) {
        any_agent_exists = true;
    }

    return any_agent_exists;
}

export function didAllAgentsShutdown() {
    let all_agents_shutdown = true;
    let all_agents = _getAllAgents();
    for (let idx in all_agents) {
        let agent = all_agents[idx];
        if (agent.stop_time === null) {
            all_agents_shutdown = false;
        }
    }

    let any_agent_exists = doesAnyAgentExist();

    return any_agent_exists && all_agents_shutdown;
}

function _getAllAgents() {
    return IslandHttpClient.get('/api/agents')
    .then(res => {
        return res.json();
    });
}
