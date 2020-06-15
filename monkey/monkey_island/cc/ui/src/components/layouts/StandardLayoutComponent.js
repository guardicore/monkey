import React from 'react'
import {Route} from 'react-router-dom'
import SideNavComponent from '../SideNavComponent'
import {Col} from 'react-bootstrap';

export const StandardLayoutComponent = ({component: Component, ...rest}) => (
  <Route {...rest} render={() => (
    <Col sm={9} md={10} smOffset={3} mdOffset={2} className='main'>
      <SideNavComponent completedSteps={rest['completedSteps']}/>
      <Component {...rest} />
    </Col>
  )}/>
)
