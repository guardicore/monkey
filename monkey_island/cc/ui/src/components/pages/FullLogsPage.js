import React from 'react';
import {Col} from 'react-bootstrap';
import JSONTree from 'react-json-tree'
import {DataTable} from 'react-data-components';

const renderJson = (val, row) => <JSONTree data={val} level={1} theme="eighties" invertTheme={true} />;
const renderTime = (val, row) => val.split('.')[0];

const columns = [
  { title: 'Type', prop: 'telem_type'  },
  { title: 'Monkey ID', prop: 'monkey_guid' },
  { title: 'Time', prop: 'timestamp', render: renderTime},
  { title: 'More Info', prop: 'data', render: renderJson, width: '40%' }
];

class FullLogsPageComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    };
  }

  componentDidMount = () => {
    fetch('/api/telemetry')
      .then(res => res.json())
      .then(res => this.setState({data: res.objects}));
  };

  render() {
    return (
      <Col xs={12}>
        <h1 className="page-title">Full Logs</h1>
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
    );
  }
}

export default FullLogsPageComponent;
