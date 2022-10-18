export enum OS {
  unknown = "unknown",
  linux = "linux",
  windows = "windows"
}

export enum CommunicationTypes {
  cc = "cc",
  scan = "scanned",
  exploited = "exploited",
  relay = "relay"
}

export type Node = {
  machine_id: number;
  connections: Connections;
}

export type Machine = {
  id: number;
  network_interfaces: string[];
  operating_system: OS;
  hostname: string;
  island: boolean;
}

export type Agent = {
  id: string;
  parent_id: number | null;
  start_time: string;
  stop_time: string | null;
}

type Connections = Record<number, CommunicationTypes[]>;

export default class MapNode {
  constructor(
    public machineId: number,
    public networkInterfaces: string[],
    public agentRunning: boolean,
    public connections: Connections,
    public operatingSystem: OS = OS.unknown,
    public hostname: string = "",
    public island: boolean = false,
    public propagatedTo: boolean = false,
    public agentId: number | null = null,
    public parentId: number | null = null) {
  }

  getGroupOperatingSystem(): OS {
    if (this.operatingSystem in OS) {
      return OS[this.operatingSystem];
    }

    return OS.unknown;
  }

  calculateNodeGroup(): string {
    let group_components = [];
    if (this.island) {
      group_components.push('island');
    }

    if (this.agentId) {
      if (!this.island && !this.parentId) {
        group_components.push('manual');
      }
      else {
        group_components.push('monkey');
      }
    }
    else if (this.propagatedTo) {
      group_components.push('propagated');
    }
    else if (!this.island) { // No "clean" for island
      group_components.push('clean');
    }

    group_components.push(this.getGroupOperatingSystem());

    if (this.agentRunning) {
      group_components.push('running');
    }

    let group = group_components.join('_');
    if (!(group in NodeGroup)) {
      return NodeGroup.clean_unknown;
    }

    return group;
  }

  getLabel(): string {
    if (this.hostname) {
      return this.hostname;
    }
    return this.networkInterfaces[0];
  }
}

export function getMachineIp(machine: Machine): string{
  return machine.network_interfaces[0].split('/')[0];
}

export enum NodeGroup {
  clean_unknown = "clean_unknown",
  clean_linux = "clean_linux",
  clean_windows = "clean_windows",
  propagated_linux = "propagated_linux",
  propagated_windows = "propagated_windows",
  island = "island",
  island_monkey_linux = "island_monkey_linux",
  island_monkey_linux_running = "island_monkey_linux_running",
  island_monkey_windows = "island_monkey_windows",
  island_monkey_windows_running = "island_monkey_windows_running",
  manual_linux = "manual_linux",
  manual_linux_running = "manual_linux_running",
  manual_windows = "manual_windows",
  manual_windows_running = "manual_windows_running",
  monkey_linux = "monkey_linux",
  monkey_linux_running = "monkey_linux_running",
  monkey_windows = "monkey_windows",
  monkey_windows_running = "monkey_windows_running"
}
