import {Button} from 'react-bootstrap';
import React from 'react';
import PropTypes from 'prop-types';

export default function nextSelectionButton(props) {
  return (
    <Button variant={'outline-monkey'} size='lg' className={'selection-button'}
            onClick={props.onButtonClick}>
      {props.text}
    </Button>
  )
}

nextSelectionButton.propTypes = {
  text: PropTypes.string,
  onButtonClick: PropTypes.func
}
