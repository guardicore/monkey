import React from 'react';
import {Button, Col} from 'react-bootstrap';
import AuthService from '../../services/AuthService';
import download from 'downloadjs';
import TelemetryLogTable from '../ui-components/TelemetryLogTable'
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

import '../../styles/pages/TelemetryPage.scss';
import {faDownload} from '@fortawesome/free-solid-svg-icons/faDownload';


class TelemetryPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();
    this.authFetch = this.auth.authFetch;
    this.state = {
      data: []
    };
  }

  downloadIslandLog = () => {
    this.authFetch('/api/log/island/download')
      .then(res => res.json())
      .then(res => {
        let filename = 'Island_log';
        let logContent = (res['log_file']);
        download(logContent, filename, 'text/plain');
      });
  };

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
            <Button bsSize="large" onClick={() => {
              this.downloadIslandLog();
            }}>
            <FontAwesomeIcon icon={faDownload}/> Download </Button>
          </div>
        </div>
      </Col>
    );
  }
}

export default TelemetryPageComponent;
