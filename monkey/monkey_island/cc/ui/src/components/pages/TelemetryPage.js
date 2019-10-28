import React from 'react';
import {Button, Col} from 'react-bootstrap';
import JSONTree from 'react-json-tree'
import {DataTable} from 'react-data-components';
import AuthComponent from '../AuthComponent';
import download from 'downloadjs'

const renderJson = (val) => <JSONTree data={val} level={1} theme="eighties" invertTheme={true} />;
const renderTime = (val) => val.split('.')[0];

const columns = [
  { title: 'Time', prop: 'timestamp', render: renderTime},
  { title: 'Monkey', prop: 'monkey'},
  { title: 'Type', prop: 'telem_catagory'},
  { title: 'Details', prop: 'data', render: renderJson, width: '40%' }
];

class TelemetryPageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    };
  }

  componentDidMount = () => {
    this.authFetch('/api/telemetry')
      .then(res => res.json())
      .then(res => this.setState({data: res.objects}));
  };

downloadIslandLog = () => {
    this.authFetch('/api/log/island/download')
      .then(res => res.json())
      .then(res => {
        let filename = 'Island_log'
        let logContent = (res['log_file']);
        download(logContent, filename, 'text/plain');
      });
    };

  render() {
    return (
    <div>
      <div>
        <Col xs={12} lg={8}>
          <h1 className="page-title">Log</h1>
          <div className="data-table-container">
            <DataTable
              keys="name"
              columns={columns}
              initialData={this.state.data}
              initialPageLength={20}
              initialSortBy={{ prop: 'timestamp', order: 'descending' }}
              pageLengthOptions={[ 20, 50, 100 ]}
            />
          </div>
        </Col>
      </div>
      <div>
        <Col xs={12} lg={8}>
          <h1 className="page-title"> Monkey Island Logs </h1>
          <div className="text-center" style={{marginBottom: '20px'}}>
            <p style={{'marginBottom': '2em', 'fontSize': '1.2em'}}> Download Monkey Island internal log file </p>
            <Button bsSize="large" onClick={()=> {
              this.downloadIslandLog();
              }}>
              <i className="glyphicon glyphicon-download"/> Download </Button>
          </div>
        </Col>
      </div>
    </div>
    );
  }
}

export default TelemetryPageComponent;
