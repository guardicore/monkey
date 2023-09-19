import React from 'react';
import SideNavComponent from '../SideNavComponent';
import {Col, Row} from 'react-bootstrap';

const SidebarLayoutComponent = ({component: Component,
                                  sideNavShow = true,
                                  sideNavDisabled = false,
                                  completedSteps = null,
                                  defaultReport = '',
                                  sideNavHeader = null,
                                  onStatusChange = () => {},
                                  onLogout = () => {},
                                  ...other
                                }) => {
    return (
      <Row id="main-row">
        {sideNavShow &&<Col sm={3} md={3} lg={3} xl={2} className='sidebar'>
          <SideNavComponent disabled={sideNavDisabled}
                            completedSteps={completedSteps}
                            defaultReport={defaultReport}
                            header={sideNavHeader}
                            onStatusChange={onStatusChange}
                            onLogout={onLogout}/>
        </Col>}
        <Component onStatusChange={onStatusChange} {...other} />
      </Row>
    )
}

export default SidebarLayoutComponent;
