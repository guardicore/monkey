import IslandHttpClient from "../IslandHttpClient";

function doesAnyAgentExist() {
    let any_agent_exists = false;
    IslandHttpClient.get('/api/agents')
        .then(res => res.json())
        .then(res => {
        if (res.length > 0) {
            any_agent_exists = true;
        }});
    return any_agent_exists;
}


function didAllAgentsShutdown() {
    let all_agents_shutdown = true;
    IslandHttpClient.get('/api/agents')
        .then(res => res.json())
        .then(res => {
        for (idx in res) {
            agent = res[idx];
            if (agent.stop_time === null) {
                all_agents_shutdown = false;
            }
        }});
    return all_agents_shutdown;
}
