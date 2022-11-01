import React from 'react';
import JSONTree from 'react-json-tree';
import MUIDataTable from 'mui-datatables';
import AuthService from '../../services/AuthService';
import '../../styles/pages/EventPage.scss';

const renderJson = (val) => <JSONTree data={val} level={1} theme="eighties" invertTheme={true}/>;
const renderTime = (val) => val.split('.')[0];

const columns = [
  {label: 'Time', name: 'timestamp'},
  {label: 'Monkey', name: 'monkey'},
  {label: 'Type', name: 'telem_category'},
  {label: 'Details',
    name: 'data',
    options: {
      setCellProps: () => ({ style: { width: '40%' }}),
      filter:false,
      sort:false
    }
  }
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
  rowsPerPageOptions: [10, 20, 50, 100],
  selectableRows: 'none'
};

class EventsTable extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();
    this.authFetch = this.auth.authFetch;
    this.state = {
      data: []
    };
  }

  componentDidMount = () => {
    this.authFetch('/api/telemetry')
      .then(res => res.json())
      .then(res => {this.setState({data: res.objects})
      })
  };

  render() {
    return (
    <>
      <div className="data-table-container">
        <MUIDataTable
          columns={columns}
          data={this.state.data.map(item => {
            return [
              renderTime(item.timestamp),
              item.monkey,
              item.telem_category,
              renderJson(item.data)
            ]})}
          options={table_options}
        />
      </div>
    </>
    );
  }
}

export default EventsTable;
