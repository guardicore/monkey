import React, {useEffect, useMemo, useState} from 'react';
import {JSONTree} from 'react-json-tree';
import '../../styles/pages/EventPage.scss';
import IslandHttpClient, {APIEndpoint} from '../IslandHttpClient';
import LoadingIcon from './LoadingIcon';
import {getEventSourceHostname, getMachineHostname, getMachineIPs} from '../utils/ServerUtils';
import {parseTimeToDateString} from '../utils/DateUtils';
import _ from 'lodash';
import {nanoid} from 'nanoid';
import XDataGrid from './XDataGrid';

const columns = [
  {headerName: 'Time', field: 'timestamp'},
  {headerName: 'Source', field: 'source'},
  {headerName: 'Target', field: 'target'},
  {headerName: 'Type', field: 'type'},
  {headerName: 'Tags', field: 'tags'},
  {headerName: 'Fields', field: 'fields', renderCell: ({value})=>{return value;}, filterable: false, sortable: false, flexValue: 1, minWidth: 250}
];

const gridInitialState = {
  sorting: {
    sortModel: [{field: 'timestamp', sort: 'desc'}]
  }
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

  return (
    <>
      <div>
        {
          loading ?
            <LoadingIcon/>
            :
            <XDataGrid
              columns={columns}
              rows={[...data]}
              initialState={{...gridInitialState}}
              maxHeight={'800px'}
              columnWidth={{min: 150, max: -1}}
            />
        }
      </div>
    </>
  );
}

export default EventsTable;
