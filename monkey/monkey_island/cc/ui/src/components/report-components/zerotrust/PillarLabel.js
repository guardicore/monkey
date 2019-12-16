import React, {Component} from 'react';
import {statusToLabelType} from './StatusLabel';
import * as PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDatabase, faUser, faWifi, faCloud, faLaptop, faEyeSlash, faCogs } from '@fortawesome/free-solid-svg-icons';

const pillarToIcon = {
  'Data': faDatabase,
  'People': faUser,
  'Networks': faWifi,
  'Workloads': faCloud,
  'Devices': faLaptop,
  'Visibility & Analytics': faEyeSlash,
  'Automation & Orchestration': faCogs
};

export default class PillarLabel extends Component {
  render() {
    const className = 'label ' + statusToLabelType[this.props.status];
    return <div className={className} style={{margin: '2px', display: 'inline-block'}}>
      <FontAwesomeIcon icon={pillarToIcon[this.props.pillar]}/> {this.props.pillar}</div>
  }
}

PillarLabel.propTypes = {
  status: PropTypes.string,
  pillar: PropTypes.string
};
