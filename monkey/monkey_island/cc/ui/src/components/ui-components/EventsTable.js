import React from 'react';
import JSONTree from 'react-json-tree';
import MUIDataTable from 'mui-datatables';
import AuthService from '../../services/AuthService';
import '../../styles/pages/EventPage.scss';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';
import LoadingIcon from './LoadingIcon';
import {getEventSourceHostname} from '../utils/ServerUtils';

const columns = [
  {label: 'Time', name: 'timestamp'},
  {label: 'Source', name: 'source'},
  {label: 'Target', name: 'target'},
  {label: 'Type', name: 'type'},
  {label: 'Tags', name: 'tags'},
  {label: 'Fields', name: 'fields',  options: {
      setCellProps: () => ({ style: { width: '30%' }}),
      filter: false,
      sort: false
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

const renderTarget = (event_target, machines) => {
  // event_target is null
  if (event_target === null) {
    return 'Local system';
  }

  // event_target is a machine ID (positive integer)
  if ((parseInt(event_target) == event_target) && (event_target > 0)) {
    for (let machine of machines) {
      if (event_target === machine['id']) {
        if ((machine['hostname'] !== null) && (machine['hostname'] !== '')) {
          return machine['hostname'];
        }
        else {
          return machine['network_interfaces'][0].split('/')[0];
        }
      }
    }
  }

  // if none of the above, event_target is an IPv4 address
  for (let machine of machines) {
    let machine_ips = machine['network_interfaces'].map(network_interface => {
      return network_interface.split('/')[0]
    })

    if (machine_ips.includes(event_target)) {
      if ((machine['hostname'] !== null) && (machine['hostname'] !== '')) {
        return machine['hostname'];
      }
      else {
        return event_target;
      }
    }
  }

  return 'Unknown';
}

const renderTags = (val) => val.join(', ');

function filterEventSpecificFields(event) {
  let filtered_event = deleteAbstractAgentEventFields(event);
  return <JSONTree data={filtered_event} level={1} theme="eighties" invertTheme={true}/>
}

function deleteAbstractAgentEventFields(myObj) {
  let abstract_agent_event_fields = ['source', 'target', 'timestamp', 'type', 'tags'];
  let tempObj = JSON.parse(JSON.stringify(myObj)); /* deepcopy */

  for (let index = 0; index < abstract_agent_event_fields.length; index++) {
    delete tempObj[abstract_agent_event_fields[index]];
  }

  return tempObj;
}

const renderEventSpecificFields = (val) => filterEventSpecificFields(val);


class EventsTable extends React.Component {
  constructor(props) {
    super(props);
    this.auth = new AuthService();
    this.authFetch = this.auth.authFetch;
    this.state = {
      events: [],
      agents: [],
      machines: [],
      loading: false
    };
  }

  componentDidMount = () => {
    this.setState({loading: true})
    IslandHttpClient.get(APIEndpoint.agents)
      .then(res => this.setState({agents: res.body}))

    IslandHttpClient.get(APIEndpoint.machines)
      .then(res => this.setState({machines: res.body}))

    IslandHttpClient.get(APIEndpoint.agentEvents)
      .then(res => this.setState({events: res.body, loading: false}))
  };

  render() {
    return (
    <>
      <div className="data-table-container">
      {
        this.state.loading ?
        <LoadingIcon/>
        :
        <MUIDataTable
          columns={columns}
          data={this.state.events.map(item => {
            return [
              renderTime(item.timestamp),
              getEventSourceHostname(item.source, this.state.agents, this.state.machines),
              renderTarget(item.target, this.state.machines),
              item.type,
              renderTags(item.tags),
              renderEventSpecificFields(item)
            ]})}
          options={table_options}
        />
      }
      </div>
    </>
    );
  }
}

export default EventsTable;
