import {Button} from 'react-bootstrap';
import React from 'react';
import PropTypes from 'prop-types';

export default function backButton(props) {
  return (
    <Button variant={'secondary'} onClick={props.onClick}>
      Back
    </Button>
  )
}

backButton.propTypes = {
  onClick: PropTypes.func
}
