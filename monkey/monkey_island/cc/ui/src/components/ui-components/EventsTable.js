import React from 'react';
import JSONTree from 'react-json-tree';
import MUIDataTable from 'mui-datatables';
import AuthService from '../../services/AuthService';
import '../../styles/pages/EventPage.scss';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';

const columns = [
  {label: 'Time', name: 'timestamp'},
  {label: 'Monkey', name: 'source'},
  {label: 'Target', name: 'target'},
  {label: 'Type', name: 'type'},
  {label: 'Tags', name: 'tags'},
  {label: 'Fields', name: 'fields',  options: {
      setCellProps: () => ({ style: { width: '30%' }}),
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

const timestamp_options =  [{year: 'numeric'}, {month: '2-digit'},{day: '2-digit'},{'hour': '2-digit'},{'minutes': '2-digit'},{'second': 'numeric'}];
const renderTime = (val) => new Date(val*1000).toLocaleString('en-us', timestamp_options);
const renderTarget = (val) => val ?  val : 'Unknown';
const renderTags = (val) => val.join(', ');

const abstract_agent_event_fields = ['source', 'target', 'timestamp', 'type', 'tags'];

function deleteKeys(myObj, array) {
  let tempObj = JSON.parse(JSON.stringify(myObj)); /* deepcopy */
  for (let index = 0; index < array.length; index++) {
        delete tempObj[array[index]];
    }
      return tempObj;
}

function setEventSpecificFields(event) {
  console.log(event);
  let filtered_event = deleteKeys(event, abstract_agent_event_fields);
  return <JSONTree data={filtered_event} level={1} theme="eighties" invertTheme={true}/>
}

const renderEventSpecificFields = (val) => setEventSpecificFields(val);

class EventsTable extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();
    this.authFetch = this.auth.authFetch;
    this.state = {
      events: []
    };
  }

  componentDidMount = () => {
    IslandHttpClient.get(APIEndpoint.agentEvents)
      .then(res => res.body)
      .then(res => {console.log(res);this.setState({events: res})
      })
  };

  render() {
    return (
    <>
      <div className="data-table-container">
        <MUIDataTable
          columns={columns}
          data={this.state.events.map(item => {
            return [
              renderTime(item.timestamp),
              item.source,
              renderTarget(item.target),
              item.type,
              renderTags(item.tags),
              renderEventSpecificFields(item)
            ]})}
          options={table_options}
        />
      </div>
    </>
    );
  }
}

export default EventsTable;
