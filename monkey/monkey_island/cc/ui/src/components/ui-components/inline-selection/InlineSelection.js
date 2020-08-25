import React from 'react';
import PropTypes from 'prop-types';
import BackButton from './BackButton';
import ManualRunOptions from '../../pages/RunMonkeyPage/ManualRunOptions';
import Container from 'react-bootstrap';


export default function InlineSelection(WrappedComponent, props, previousComponent){
  return (
    <Container className={'inline-selection-component'}>
      {previousComponent === undefined ? '' :
        <BackButton onClick={() => {setPreviousComponent(props, previousComponent)}}/>}
      <WrappedComponent {...props}/>
    </Container>
  )
}

function setPreviousComponent(props, previousComponent) {
  if(previousComponent === ManualRunOptions){
    return props.setComponent()
  } else {
    return props.setComponent(previousComponent, props)
  }
}

InlineSelection.propTypes = {
  setComponent: PropTypes.func,
  ips: PropTypes.arrayOf(PropTypes.string)
}
