function getJSRuntimePort() {
    return process.env.NEXT_PUBLIC_JAVASCRIPT_RUNTIME_PORT;
}

export const JS_RUNTIME_PORT = getJSRuntimePort();
