import React from 'react';

// Boilerplate code to inject properties into the SignInPage component
// https://legacy.reactjs.org/docs/higher-order-components.html#convention-pass-unrelated-props-through-to-the-wrapped-component
export const injectProperties = (
    WrappedComponent: React.FC,
    additionalProperties: { [key: string]: any }
) => {
    const Wrapper = ({ ...props }) => {
        return <WrappedComponent {...props} {...additionalProperties} />;
    };
    return Wrapper;
};
