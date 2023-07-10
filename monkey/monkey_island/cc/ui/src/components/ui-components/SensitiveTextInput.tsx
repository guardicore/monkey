import React, { useState } from 'react';
import { FormControl } from 'react-bootstrap';
import SensitiveInput from './SensitiveInput';

function SensitiveTextInput(props) {
    const [hidden, setHidden] = useState(false);

    const onChange = (value) => {
        return props.onChange(value === '' ? props.options.emptyValue : value);
    };

    let inputComponent = (
        <FormControl
            value={props.value || ''}
            type={hidden ? 'text' : 'password'}
            onChange={(event) => onChange(event.target.value)}
        />
    );

    return (
        <SensitiveInput
            inputComponent={inputComponent}
            toggle={() => setHidden(!hidden)}
            hidden={hidden}
        />
    );
}

export default SensitiveTextInput;
