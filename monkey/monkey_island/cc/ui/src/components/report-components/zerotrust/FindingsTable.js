import React, {Component, Fragment} from 'react';
import StatusLabel from './StatusLabel';
import PaginatedTable from '../common/PaginatedTable';
import * as PropTypes from 'prop-types';
import PillarLabel from './PillarLabel';
import EventsButton from './EventsButton';
import ScoutSuiteRuleButton from './scoutsuite/ScoutSuiteRuleButton';

const EVENTS_COLUMN_MAX_WIDTH = 180;
const PILLARS_COLUMN_MAX_WIDTH = 260;


export class FindingsTable extends Component {
  columns = [
    {
      columns: [
        {
          Header: 'Finding', accessor: 'test',
          style: {'whiteSpace': 'unset'}  // This enables word wrap
        },

        {
          Header: 'Details', id: 'details',
          accessor: x => this.getFindingDetails(x),
          maxWidth: EVENTS_COLUMN_MAX_WIDTH
        },

        {
          Header: 'Pillars', id: 'pillars',
          accessor: x => this.getFindingPillars(x),
          maxWidth: PILLARS_COLUMN_MAX_WIDTH,
          style: {'whiteSpace': 'unset'}
        }
      ]
    }
  ];

  getFindingDetails(finding) {
    if (finding.finding_type === 'scoutsuite_finding') {
      return <ScoutSuiteRuleButton scoutsuite_rules={finding.details.scoutsuite_rules}
                                   scoutsuite_data={this.props.scoutsuite_data}/>;
    } else if (finding.finding_type === 'monkey_finding') {
      return <EventsButton finding_id={finding.finding_id}
                           latest_events={finding.details.latest_events}
                           oldest_events={finding.details.oldest_events}
                           event_count={finding.details.event_count}
                           exportFilename={'Events_' + finding.test_key}/>;
    }
  }

  getFindingPillars(finding) {
    const pillars = finding.pillars;
    const pillarLabels = pillars.map((pillar) =>
      <PillarLabel key={pillar.name} pillar={pillar.name} status={pillar.status}/>
    );
    return <div style={{textAlign: 'center'}}>{pillarLabels}</div>;
  }

  render() {
    return <Fragment>
      <h3>{<span style={{display: 'inline-block'}}><StatusLabel status={this.props.status} showText={true}/>
      </span>} tests' findings</h3>
      <PaginatedTable data={this.props.data} pageSize={10} columns={this.columns}/>
    </Fragment>
  }
}

FindingsTable.propTypes = {data: PropTypes.array, status: PropTypes.string};
