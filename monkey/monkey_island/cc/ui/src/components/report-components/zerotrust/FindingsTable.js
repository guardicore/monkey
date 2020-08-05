import React, {Component, Fragment} from 'react';
import StatusLabel from './StatusLabel';
import PaginatedTable from '../common/PaginatedTable';
import * as PropTypes from 'prop-types';
import PillarLabel from './PillarLabel';
import EventsButton from './EventsButton';

const EVENTS_COLUMN_MAX_WIDTH = 170;
const PILLARS_COLUMN_MAX_WIDTH = 200;
const columns = [
  {
    columns: [
      {
        Header: 'Finding', accessor: 'test',
        style: {'whiteSpace': 'unset'}  // This enables word wrap
      },

      {
        Header: 'Events', id: 'events',
        accessor: x => {
          return <EventsButton finding_id={x.finding_id}
                               latest_events={x.latest_events}
                               oldest_events={x.oldest_events}
                               event_count={x.event_count}
                               exportFilename={'Events_' + x.test_key} />;
        },
        maxWidth: EVENTS_COLUMN_MAX_WIDTH
      },

      {
        Header: 'Pillars', id: 'pillars',
        accessor: x => {
          const pillars = x.pillars;
          const pillarLabels = pillars.map((pillar) =>
            <PillarLabel key={pillar.name} pillar={pillar.name} status={pillar.status}/>
          );
          return <div style={{textAlign: 'center'}}>{pillarLabels}</div>;
        },
        maxWidth: PILLARS_COLUMN_MAX_WIDTH,
        style: {'whiteSpace': 'unset'}
      }
    ]
  }
];


export class FindingsTable extends Component {
  render() {
    return <Fragment>
      <h3>{<span style={{display: 'inline-block'}}><StatusLabel status={this.props.status} showText={true}/>
      </span>} tests' findings</h3>
      <PaginatedTable data={this.props.data} pageSize={10} columns={columns}/>
    </Fragment>
  }
}

FindingsTable.propTypes = {data: PropTypes.array, status: PropTypes.string};
