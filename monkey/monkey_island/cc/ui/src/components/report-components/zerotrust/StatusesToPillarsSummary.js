import React, {Component, Fragment} from 'react';
import PillarLabel from './PillarLabel';
import StatusLabel from './StatusLabel';
import * as PropTypes from 'prop-types';
import {ZeroTrustStatuses} from './ZeroTrustPillars';

export default class StatusesToPillarsSummary extends Component {
  render() {
    return (<div id="piilar-summary">
      {this.getStatusSummary(ZeroTrustStatuses.failed)}
      {this.getStatusSummary(ZeroTrustStatuses.verify)}
      {this.getStatusSummary(ZeroTrustStatuses.passed)}
      {this.getStatusSummary(ZeroTrustStatuses.unexecuted)}
    </div>);
  }

  getStatusSummary(status) {
    if (this.props.statusesToPillars[status].length > 0) {
      return <Fragment>
        <h3>
          <StatusLabel showText={true} status={status}/>
        </h3>
        <div>
          {
            this.props.statusesToPillars[status].map((pillar) => {
              return <PillarLabel key={pillar} pillar={pillar} status={status}/>
            })
          }
        </div>
      </Fragment>
    }
  }
}

StatusesToPillarsSummary.propTypes = {
  statusesToPillars: PropTypes.object
};
