import React, {Component} from 'react';
import SinglePillarPrinciplesStatus from './SinglePillarPrinciplesStatus';
import * as PropTypes from 'prop-types';

export default class PrinciplesSection extends Component {
  render() {
    return <div id="principles-section">
      <h2>Test Results</h2>
      <p>
        The <a href="https://www.forrester.com/report/The+Zero+Trust+eXtended+ZTX+Ecosystem/-/E-RES137210">
        Zero Trust eXtended (ZTX) framework
      </a> is composed of 7 pillars. Each pillar is built of
        several guiding principles tested by the Infection Monkey.
      </p>
      {
        Object.keys(this.props.principles).map((pillar) =>
          <SinglePillarPrinciplesStatus
            key={pillar}
            pillar={pillar}
            principlesStatus={this.props.principles[pillar]}
            pillarsToStatuses={this.props.pillarsToStatuses}/>
        )
      }
    </div>
  }
}

PrinciplesSection.propTypes = {
  principles: PropTypes.object,
  pillarsToStatuses: PropTypes.object
};
