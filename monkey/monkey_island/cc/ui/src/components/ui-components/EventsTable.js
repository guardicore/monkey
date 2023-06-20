import React, {useEffect, useMemo, useState} from 'react';
import {JSONTree} from 'react-json-tree';
import {
  DataGrid,
  gridFilteredTopLevelRowCountSelector,
  GridToolbar
} from '@mui/x-data-grid';
import '../../styles/pages/EventPage.scss';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';
import LoadingIcon from './LoadingIcon';
import {getEventSourceHostname, getMachineHostname, getMachineIPs} from '../utils/ServerUtils';
import {parseTimeToDateString} from '../utils/DateUtils';
import _ from 'lodash';
import {nanoid} from 'nanoid';
import CustomNoRowsOverlay from './utils/GridNoRowsOverlay';

const columns = [
  {headerName: 'Time', field: 'timestamp', flex: 0.5, minWidth: '150px'},
  {headerName: 'Source', field: 'source', flex: 0.5, minWidth: '150px'},
  {headerName: 'Target', field: 'target', flex: 0.5, minWidth: '150px'},
  {headerName: 'Type', field: 'type', flex: 0.5, minWidth: '150px'},
  {headerName: 'Tags', field: 'tags', flex: 0.5, minWidth: '150px'},
  {headerName: 'Fields', field: 'fields', renderCell: ({value})=>{return value;}, filterable: false, sortable: false, flex: 1, minWidth: '200px'}
];

const gridInitialState = {
  sorting: {
    sortModel: [{field: 'timestamp', sort: 'desc'}]
  },
  pagination: {paginationModel: {pageSize: 10}}
};

const renderTime = (val) => parseTimeToDateString(val * 1000);

const renderTarget = (event_target, machines) => {
  // event_target is null
  if (event_target === null) {
    return 'Local system';
  }

  // event_target is a machine ID (positive integer)
  if ((parseInt(event_target) === event_target) && (event_target > 0)) {
    for (let machine of machines) {
      if (event_target === machine['id']) {
        return getMachineHostname(machine);
      }
    }
  }

  // if none of the above, event_target is an IPv4 address
  for (let machine of machines) {
    let machine_ips = getMachineIPs(machine);

    if (machine_ips.includes(event_target)) {
      if ((machine['hostname'] !== null) && (machine['hostname'] !== '')) {
        return machine['hostname'];
      } else {
        return event_target;
      }
    }
  }

  return 'Unknown';
}

const renderTags = (val) => val.join(', ');

function formatEventFields(event) {
  let filtered_event = deleteAbstractAgentEventFields(event);
  let formatted_event = redactSecretsInEventFields(filtered_event);

  return <JSONTree data={formatted_event} level={1} theme="eighties" invertTheme={true}/>
}

function deleteAbstractAgentEventFields(myObj) {
  let abstract_agent_event_fields = ['source', 'target', 'timestamp', 'type', 'tags'];
  let tempObj = _.cloneDeep(myObj)

  for (let index = 0; index < abstract_agent_event_fields.length; index++) {
    delete tempObj[abstract_agent_event_fields[index]];
  }

  return tempObj;
}

function redactSecretsInEventFields(myObj) {
  let tempObj = _.cloneDeep(myObj);

  let stolenCredentialsFieldName = 'stolen_credentials';
  let secretFieldName = 'secret';

  if (_.has(tempObj, stolenCredentialsFieldName)) {
    for (let stolenCredential of tempObj[stolenCredentialsFieldName]) {
      let secrets = stolenCredential[secretFieldName];
      for (let secretType in secrets) {
        let redactedSecret = '*'.repeat(stolenCredential[secretFieldName][secretType].length);
        stolenCredential[secretFieldName][secretType] = redactedSecret;
      }
    }
  }

  return tempObj;
}


const EventsTable = () => {
  const [events, setEvents] = useState([]);
  const [agents, setAgents] = useState([]);
  const [machines, setMachines] = useState([]);
  const [loading, setLoading] = useState(false);
  const [gridVisibleFilteredRowsCount, setGridVisibleFilteredRowsCount] = useState(0);

  const data = useMemo(() => {
    return events.map(item => {
      return {
        id: nanoid(),
        timestamp: renderTime(item.timestamp),
        source: getEventSourceHostname(item.source, agents, machines),
        target: renderTarget(item.target, machines),
        type: item.type,
        tags: renderTags(item.tags),
        fields: formatEventFields(item)
      }
    });
  }, [events]);

  useEffect(() => {
    setLoading(true);

    IslandHttpClient.getJSON(APIEndpoint.agents, {}, true)
      .then(res => setAgents(res.body));

    IslandHttpClient.getJSON(APIEndpoint.machines, {}, true)
      .then(res => setMachines(res.body));

    IslandHttpClient.getJSON(APIEndpoint.agentEvents, {}, true)
      .then(res => {
        setLoading(false);
        setEvents(res.body);
      });
  }, []);

  const handleGridState = (state) => {
    console.log(state);
    const visibleFilteredRowsCount = state ? (gridFilteredTopLevelRowCountSelector(state) || 0) : 0;
    setGridVisibleFilteredRowsCount(visibleFilteredRowsCount);
  }

  return (
    <>
      <div className="data-table-container" style={{height: `${!data?.length || !gridVisibleFilteredRowsCount ? '300px' : 'auto'}`}}>
        {
          loading ?
            <LoadingIcon/>
            :
            <DataGrid
              onStateChange={handleGridState}
              columns={columns}
              rows={[...data]}
              initialState={{...gridInitialState}}
              pageSizeOptions={[10, 25, 50, 100]}
              getRowHeight={() => 'auto'}
              slots={{
                toolbar: GridToolbar,
                noRowsOverlay: CustomNoRowsOverlay,
                noResultsOverlay: CustomNoRowsOverlay
              }}
              disableRowSelectionOnClick
            />
        }
      </div>
    </>
  );
}

export default EventsTable;
