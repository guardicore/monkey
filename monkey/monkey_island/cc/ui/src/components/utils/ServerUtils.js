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
