export enum OS {
  unknown = "unknown",
  linux = "linux",
  windows = "windows"
}

export enum CommunicationTypes {
  cc = "cc",
  scan = "scan",
  exploited = "exploited"
  tunnel = "tunnel"
}

export class MapNode {
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

export enum NodeGroup {
    clean_unknown,
    clean_linux,
    clean_windows,
    propagated_linux,
    propagated_windows,
    island,
    island_monkey_linux,
    island_monkey_linux_running,
    island_monkey_windows,
    island_monkey_windows_running,
    manual_linux,
    manual_linux_running,
    manual_windows,
    manual_windows_running,
    monkey_linux,
    monkey_linux_running,
    monkey_windows,
    monkey_windows_running
}
