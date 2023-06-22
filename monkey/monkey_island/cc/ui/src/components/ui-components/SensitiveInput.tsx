import React from 'react';
import {InputGroup} from 'react-bootstrap';

function SensitiveTextInput(props){

    return (
      <InputGroup>
        {props.inputComponent}
        <InputGroup.Append style={{display: 'flex'}}>
          <InputGroup.Text onClick={props.toggle} style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0}} >
            <i className={props.hidden ? 'fas fa-eye-slash' : 'fas fa-eye'}></i>
          </InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>
    );
}

export default SensitiveTextInput;
