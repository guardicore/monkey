import React from 'react';
import {Route} from 'react-router-dom';
import SideNavComponent from '../SideNavComponent';
import {Col, Row} from 'react-bootstrap';

const SidebarLayoutComponent = ({component: Component,
                                  sideNavShow = true,
                                  sideNavDisabled = false,
                                  completedSteps = null,
                                  defaultReport = '',
                                  sideNavHeader = (<></>),
                                  ...other
                                }) => (
  <Route {...other} render={() => {
    return (
      <Row>
        {sideNavShow &&<Col sm={3} md={3} lg={3} xl={2} className='sidebar'>
          <SideNavComponent disabled={sideNavDisabled}
                            completedSteps={completedSteps}
                            defaultReport={defaultReport}
                            header={sideNavHeader}/>
        </Col>}
        <Component {...other} />
      </Row>)
  }}/>
)

export default SidebarLayoutComponent;
