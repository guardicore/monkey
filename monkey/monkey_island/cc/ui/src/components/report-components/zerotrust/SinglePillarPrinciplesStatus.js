import AuthComponent from '../../AuthComponent';
import PillarLabel from './PillarLabel';
import PrinciplesStatusTable from './PrinciplesStatusTable';
import React from 'react';
import * as PropTypes from 'prop-types';
import {Panel} from 'react-bootstrap';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronDown } from '@fortawesome/free-solid-svg-icons';

export default class SinglePillarPrinciplesStatus extends AuthComponent {
  render() {
    if (this.props.principlesStatus.length === 0) {
      return null;
    } else {
      return (
        <Panel>
          <Panel.Heading>
            <Panel.Title toggle>
              <h3 style={{textAlign: 'center', marginTop: '1px', marginBottom: '1px'}}>
                <FontAwesomeIcon icon={faChevronDown}/> <PillarLabel pillar={this.props.pillar}
                                                                 status={this.props.pillarsToStatuses[this.props.pillar]}/>
              </h3>
            </Panel.Title>
          </Panel.Heading>
          <Panel.Collapse>
            <Panel.Body>
              <PrinciplesStatusTable principlesStatus={this.props.principlesStatus}/>
            </Panel.Body>
          </Panel.Collapse>
        </Panel>
      );
    }
  }
}

SinglePillarPrinciplesStatus.propTypes = {
  principlesStatus: PropTypes.array,
  pillar: PropTypes.string
};
