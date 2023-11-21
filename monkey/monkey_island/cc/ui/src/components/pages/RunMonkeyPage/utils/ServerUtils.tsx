function getNodePort() {
    return process.env.JAVASCRIPT_RUNTIME_PORT;
}

export const NODE_PORT = getNodePort();
