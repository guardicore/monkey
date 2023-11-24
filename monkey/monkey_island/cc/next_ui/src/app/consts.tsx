function getJSRuntimePort() {
    // TODO remove with the NEXT_JS_UI_FEATURE in monkey_island/cc/feature_flags.py:1
    return process.env.NEXT_PUBLIC_JAVASCRIPT_RUNTIME_PORT || 5000;
}

export const JS_RUNTIME_PORT = getJSRuntimePort();
