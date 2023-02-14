import React, {useState} from 'react';
import {InputGroup, FormControl} from 'react-bootstrap';

function SensitiveTextareaInput(props){
    const [hidden, setHidden] = useState(false);

    const toggleShow = () =>{
        setHidden(! hidden);
    }

    const onChange = (value) => {
        return props.onChange(value === '' ? props.options.emptyValue : value);
    }

    return (
    <div>
      <InputGroup>
        <FormControl
            as="textarea"
            rows={5}
            className={hidden ? '' : 'password'}
            value={props.value || ''}
            onChange={(event) => onChange(event.target.value)}
        />
        <InputGroup.Append>
          <InputGroup.Text onClick={toggleShow} >
            <i className={hidden ? 'fas fa-eye-slash' : 'fas fa-eye'}></i>
          </InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>
    </div>
    );
}

export default SensitiveTextareaInput;
