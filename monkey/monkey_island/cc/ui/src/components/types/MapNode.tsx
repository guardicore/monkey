export enum OS {
  unknown="unknown",
  linux="linux",
  windows="windows"
}

export enum CommunicationTypes {
  cc = "cc",
  scanned = "scanned",
  exploited = "exploited"
}

export default class MapNode {
  constructor(
    public machine_id: number,
    public network_interfaces: string[],
    public agent_is_running: boolean,
    public connections: Record<string, CommunicationTypes[]>,
    public operating_system: OS = OS.unknown,
    public hostname: string = "",
    public island: boolean = false,
    public propagated_to: boolean = false,
    public agent_id: string = null,
    public parent_id: string = null) {
  }
}
