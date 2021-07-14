import React from 'react';
import {Route} from 'react-router-dom';
import SideNavComponent from '../SideNavComponent.tsx';
import {Col, Row} from 'react-bootstrap';

export const DisabledSidebarLayoutComponent = ({component: Component, ...rest}) => (
  <Route {...rest} render={() => (
    <Row>
      <Col sm={3} md={3} lg={3} xl={2} className='sidebar'>
        <SideNavComponent disabled={true} completedSteps={rest['completedSteps']}/>
      </Col>
      <Component {...rest} />
    </Row>
    )}/>
)
