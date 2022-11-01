import React from 'react';
import {Col} from 'react-bootstrap';
import AuthService from '../../services/AuthService';
import TelemetryLogTable from '../ui-components/TelemetryLogTable'

import '../../styles/pages/TelemetryPage.scss';


class EventPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();
    this.authFetch = this.auth.authFetch;
    this.state = {
      data: []
    };
  }

  render() {
    return (
      <Col sm={{offset: 3, span: 9}} md={{offset: 3, span: 9}}
           lg={{offset: 3, span: 9}} xl={{offset: 2, span: 7}}
           className={'main'}>
        <div>
          <h1 className="page-title">Agent telemetries</h1>
          <TelemetryLogTable/>
        </div>
      </Col>
    );
  }
}

export default EventPageComponent;
