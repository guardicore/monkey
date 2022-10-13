import IslandHttpClient from "../IslandHttpClient";

export function doesAnyAgentExist() {
    let any_agent_exists = false;
    all_agents = _getAllAgents();
    if (all_agents.length > 0) {
        any_agent_exists = true;
    }
    return any_agent_exists;
}

export function didAllAgentsShutdown() {
    let all_agents_shutdown = true;
    all_agents = _getAllAgents();
    for (idx in all_agents) {
        agent = all_agents[idx];
        if (agent.stop_time === null) {
            all_agents_shutdown = false;
        }
    }
    return all_agents_shutdown;
}

function _getAllAgents() {
    return IslandHttpClient.get('/api/agents')
    .then(res => {
        return res.json();
    });
}
