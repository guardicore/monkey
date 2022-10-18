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

export class MapNode {
  constructor(
    public machine_id: number,
    public network_interfaces: string[],
    public agent_is_running: boolean,
    public connections: Record<number, CommunicationTypes[]>,
    public operating_system: OS = OS.unknown,
    public hostname: string = "",
    public island: boolean = false,
    public propagated_to: boolean = false,
    public agent_id: string = null,
    public parent_id: string = null) {
  }

  getGroupOperatingSystem(): OS {
    if (this.operating_system in OS) {
      return OS[this.operating_system];
    }

    return OS.unknown;
  }

  calculateNodeGroup(): string {
    let group_components = [];
    if (this.island) {
      group_components.push('island');
    }

    if (this.agent_id) {
      if (!this.island && !this.parent_id) {
        group_components.push('manual');
      }
      else {
        group_components.push('monkey');
      }
    }
    else if (this.propagated_to) {
      group_components.push('propagated');
    }
    else if (!this.island) { // No "clean" for island
      group_components.push('clean');
    }

    group_components.push(this.getGroupOperatingSystem());

    if (this.agent_is_running) {
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
    return this.network_interfaces[0];
  }
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
