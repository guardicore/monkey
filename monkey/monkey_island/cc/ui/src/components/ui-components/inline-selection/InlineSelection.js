import React from 'react';
import PropTypes from 'prop-types';
import BackButton from './BackButton';
import {Col, Row, Container} from 'react-bootstrap';


export default function InlineSelection(WrappedComponent, props) {
  return (
    <Container className={'inline-selection-component'}>
      <Row>
        <Col lg={8} md={10} sm={12}>
          <WrappedComponent {...props}/>
          {renderBackButton(props)}
        </Col>
      </Row>
    </Container>
  )
}

function renderBackButton(props){
  if(props.onBackButtonClick !== undefined){
    return (<BackButton onClick={props.onBackButtonClick}/>);
  }
}

InlineSelection.propTypes = {
  setComponent: PropTypes.func,
  ips: PropTypes.arrayOf(PropTypes.string),
  onBackButtonClick: PropTypes.func
}
