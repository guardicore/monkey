import React from 'react';
import {Button, Col} from 'react-bootstrap';
import JSONTree from 'react-json-tree';
import MUIDataTable from 'mui-datatables';
import AuthComponent from '../AuthComponent';
import download from 'downloadjs';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

import '../../styles/pages/TelemetryPage.scss';
import {faDownload} from '@fortawesome/free-solid-svg-icons/faDownload';

const renderJson = (val) => <JSONTree data={val} level={1} theme="eighties" invertTheme={true}/>;
const renderTime = (val) => val.split('.')[0];

const columns = [
  {label: 'Time', name: 'timestamp'},
  {label: 'Monkey', name: 'monkey'},
  {label: 'Type', name: 'telem_category'},
  {label: 'Details', name: 'data', options: { setCellProps: () => ({ style: { width: '40%' }})}}
];

const table_options = {
    filterType: 'textField',
    sortOrder: {
        name: 'timestamp',
        direction: 'desc'
      },
    print: false,
    download: false,
    rowHover: false,
    rowsPerPage: 20,
    rowsPerPageOptions: [20, 50, 100],
    selectableRows: 'none'
  };

class TelemetryPageComponent extends AuthComponent {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      isFetching: false
    };
  }

  componentDidMount = () => {
    this.authFetch('/api/telemetry')
      .then(res => res.json())
      .then(res => {this.setState({data: res.objects})
      })
      .catch(e => {
        console.log(e);
        this.setState({...this.state});
      });
  };

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
          <div className="data-table-container">
            <MUIDataTable
              columns={columns}
              data={this.state.data.map(item => {
                return [
                  renderTime(item.timestamp),
                  item.monkey,
                  item.telem_category,
                  renderJson(item.data)
                  ]
                })
                }
                options={table_options}
            />
          </div>
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
