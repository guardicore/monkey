import React, {useState} from 'react';
import {InputGroup, FormControl} from 'react-bootstrap';

function SensitiveTextInput(props){

    return (
    <div>
      <InputGroup>
        {props.inputComponent}
        <InputGroup.Append>
          <InputGroup.Text onClick={props.toggle} >
            <i className={props.hidden ? 'fas fa-eye-slash' : 'fas fa-eye'}></i>
          </InputGroup.Text>
        </InputGroup.Append>
      </InputGroup>
    </div>
    );
}

export default SensitiveTextInput;
