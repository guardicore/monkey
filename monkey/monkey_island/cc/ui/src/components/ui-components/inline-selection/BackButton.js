import {Button, Col, Row} from 'react-bootstrap';
import React from 'react';
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCaretLeft} from '@fortawesome/free-solid-svg-icons/faCaretLeft';

export default function backButton(props) {
  return (
    <Row>
      <Col>
        <Button variant={'outline-dark'} onClick={props.onClick} className={'back-button'}>
          <FontAwesomeIcon icon={faCaretLeft} />
          <h1>Back</h1>
        </Button>
      </Col>
    </Row>
  )
}

backButton.propTypes = {
  onClick: PropTypes.func
}
