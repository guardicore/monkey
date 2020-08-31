import {Button, Row, Col} from 'react-bootstrap';
import React from 'react';
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faAngleRight} from '@fortawesome/free-solid-svg-icons';

export default function nextSelectionButton(props) {
  let description = props.description !== undefined ? (<p>{props.description}</p>) : ''
  let icon = props.icon !== undefined ? (<FontAwesomeIcon icon={props.icon}/>) : ''
  return (
    <Row>
      <Col>
        <Button variant={'outline-monkey'} size='lg' className={'selection-button'}
                onClick={props.onButtonClick}>
          {icon}
          <h1>{props.text}</h1>
          {description}
          <FontAwesomeIcon icon={faAngleRight} className={'angle-right'}/>
        </Button>
      </Col>
    </Row>
  )
}

nextSelectionButton.propTypes = {
  text: PropTypes.string,
  icon: FontAwesomeIcon,
  onButtonClick: PropTypes.func
}
