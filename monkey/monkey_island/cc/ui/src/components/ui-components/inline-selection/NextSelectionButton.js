import {Button, Row, Col} from 'react-bootstrap';
import React from 'react';
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faAngleRight} from '@fortawesome/free-solid-svg-icons';

export default function nextSelectionButton(props) {
  let description = props.description !== undefined ? (<p>{props.description}</p>) : ''
  let iconType = props.iconType !== undefined ? props.iconType : ''
  let icon = props.icon !== undefined ? (<FontAwesomeIcon className={iconType} icon={props.icon}/>) : ''
  return (
    <Row>
      <Col>
        <Button variant={'outline-monkey'} size='lg' className={'selection-button'}
                onClick={props.onButtonClick}>
          <div className="selection-button-content-wrapper">
            <div className="selection-button-details-wrapper">
              <div className="selection-button-title">
                {icon}
                <h1>{props.title}</h1>
              </div>
              <div className="selection-button-description">
                {description}
              </div>
            </div>
            <div className="selection-button-side-icon">
              <FontAwesomeIcon icon={faAngleRight} className={'angle-right'}/>
            </div>
          </div>
        </Button>
      </Col>
    </Row>
  )
}

nextSelectionButton.propTypes = {
  title: PropTypes.string,
  iconType: PropTypes.string,
  icon: FontAwesomeIcon,
  description: PropTypes.string,
  onButtonClick: PropTypes.func
}
