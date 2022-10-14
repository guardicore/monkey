export class MapNode {
    machine_id: number
    operating_system: string
    hostname: string
    network_interfaces: object
    agent_is_running: boolean
    island: boolean
    propagated_to: boolean
    connections: object
    agent_id?: string
    parent_id?: string

    constructor(machine_id: number,
        operating_system: string,
        hostname: string,
        network_interfaces: object,
        agent_is_running: boolean,
        island: boolean,
        propagated_to: boolean,
        connections: object,
        agent_id?: string,
        parent_id?: string) {
        this.machine_id = machine_id
        this.operating_system = operating_system
        this.hostname = hostname
        this.network_interfaces = network_interfaces
        this.agent_is_running = agent_is_running
        this.island = island
        this.propagated_to = propagated_to
        this.connections = connections
        this.agent_id = agent_id
        this.parent_id = parent_id
    }
}
