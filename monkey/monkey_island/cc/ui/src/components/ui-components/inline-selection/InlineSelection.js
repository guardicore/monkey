import React from 'react';
import PropTypes from 'prop-types';
import BackButton from './BackButton';
import ManualRunOptions from '../../pages/RunMonkeyPage/ManualRunOptions';
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
  } else if(props.previousComponent === undefined){
    return (<BackButton onClick={() => {setPreviousComponent(props, props.previousComponent)}}/>);
  }
}

function setPreviousComponent(props) {
  if (props.previousComponent === ManualRunOptions) {
    return props.setComponent()
  } else {
    return props.setComponent(props.previousComponent, props)
  }
}

InlineSelection.propTypes = {
  setComponent: PropTypes.func,
  ips: PropTypes.arrayOf(PropTypes.string),
  previousComponent: PropTypes.object,
  onBackButtonClick: PropTypes.func
}
