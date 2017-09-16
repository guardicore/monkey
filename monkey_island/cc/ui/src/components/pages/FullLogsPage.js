import React from 'react';
import {Col} from 'react-bootstrap';
import JSONTree from 'react-json-tree'
import {DataTable} from 'react-data-components';

const renderJson = (val) => <JSONTree data={val} level={1} theme="eighties" invertTheme={true} />;
const renderTime = (val) => val.split('.')[0];

const columns = [
  { title: 'Time', prop: 'timestamp', render: renderTime},
<<<<<<< HEAD
  { title: 'Monkey ID', prop: 'monkey_guid' },
  { title: 'Type', prop: 'telem_type'  },
  { title: 'More Info', prop: 'data', render: renderJson, width: '40%' }
=======
  { title: 'Monkey', prop: 'monkey' },
  { title: 'Type', prop: 'telem_type'  },
  { title: 'Details', prop: 'data', render: renderJson, width: '40%' }
>>>>>>> e37a0a98630fdd673166aa7d149031db577946cd
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
        <h1 className="page-title">Monkey Telemetry</h1>
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
