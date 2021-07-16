import React from 'react';
import {Route} from 'react-router-dom';
import SideNavComponent from '../SideNavComponent.tsx';
import {Col, Row} from 'react-bootstrap';

const SidebarLayoutComponent = ({component: Component,
                                  sideNavDisabled = false,
                                  completedSteps = null,
                                  ...other
                                }) => (
  <Route {...other} render={() => {
    return (
      <Row>
        <Col sm={3} md={3} lg={3} xl={2} className='sidebar'>
          <SideNavComponent disabled={sideNavDisabled} completedSteps={completedSteps}/>
        </Col>
        <Component {...other} />
      </Row>)
  }}/>
)

export default SidebarLayoutComponent;
