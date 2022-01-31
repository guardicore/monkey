import React from 'react';
import {Col} from 'react-bootstrap';
import AuthService from '../../services/AuthService';
import TelemetryLogTable from '../ui-components/TelemetryLogTable'

import '../../styles/pages/TelemetryPage.scss';
import {IslandLogDownloadButton} from '../ui-components/LogDownloadButtons';


class TelemetryPageComponent extends React.Component {
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
          <h1 className="page-title">Logs</h1>
          <TelemetryLogTable/>
        </div>
        <div>
          <h1 className="page-title"> Monkey Island Logs </h1>
          <div className="text-center" style={{marginBottom: '20px'}}>
            <p style={{'marginBottom': '2em', 'fontSize': '1.2em'}}> Download Monkey Island internal log file </p>
            <IslandLogDownloadButton url={'/api/log/island/download'}/>
          </div>
        </div>
      </Col>
    );
  }
}

export default TelemetryPageComponent;
