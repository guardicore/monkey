function getJSRuntimePort() {
    return process.env.JAVASCRIPT_RUNTIME_PORT;
}

export const JS_RUNTIME_PORT = getJSRuntimePort();
