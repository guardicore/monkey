export type LoginParams = {
    username: string;
    password: string;
};

export type ExploitationConfiguration = {
    exploiters: object;
};

export type ICMPScanConfiguration = {
    timeout: number;
};

export type NetworkScanConfiguration = {
    targets: ScanTargetConfiguration;
    icmp: ICMPScanConfiguration;
    tcp: TCPScanConfiguration;
    fingerprinters: object;
};

export type PolymorphismConfiguration = {
    randomize_agent_hash: boolean;
};

export type PropagationConfiguration = {
    maximum_depth: number;
    network_scan: NetworkScanConfiguration;
    exploitation: ExploitationConfiguration;
};

export type ScanTargetConfiguration = {
    scan_my_networks: boolean;
    subnets: string[];
    blocked_ips: string[];
    inaccessible_subnets: string[];
};

export type TCPScanConfiguration = {
    ports: number[];
    timeout: number;
};

export type AgentConfiguration = {
    keep_tunnel_open_time: number;
    credentials_collectors: object;
    payloads: object;
    propagation: PropagationConfiguration;
    polymorphism: PolymorphismConfiguration;
};

export type RegistrationStatus = {
    needs_registration: boolean;
};
