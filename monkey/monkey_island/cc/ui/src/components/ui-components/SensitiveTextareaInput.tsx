import React, { useState } from 'react';
import { FormControl } from 'react-bootstrap';
import SensitiveInput from './SensitiveInput';

function SensitiveTextareaInput(props) {
    const [hidden, setHidden] = useState(false);

    const onChange = (value) => {
        return props.onChange(value === '' ? props.options.emptyValue : value);
    };

    let inputComponent = (
        <FormControl
            as="textarea"
            rows={5}
            className={hidden ? '' : 'password'}
            value={props.value || ''}
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

export default SensitiveTextareaInput;
