import React, {Component} from 'react';
import {statusToLabelType} from './StatusLabel';
import * as PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDatabase } from '@fortawesome/free-solid-svg-icons/faDatabase';
import { faUser  } from '@fortawesome/free-solid-svg-icons/faUser';
import { faWifi } from '@fortawesome/free-solid-svg-icons/faWifi';
import { faCloud } from '@fortawesome/free-solid-svg-icons/faCloud';
import { faLaptop } from '@fortawesome/free-solid-svg-icons/faLaptop';
import { faEyeSlash } from '@fortawesome/free-solid-svg-icons/faEyeSlash';
import { faCogs } from '@fortawesome/free-solid-svg-icons/faCogs';

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
    const className = 'badge ' + statusToLabelType[this.props.status];
    return <div className={className} style={{margin: '2px', display: 'inline-block'}}>
      <FontAwesomeIcon icon={pillarToIcon[this.props.pillar]}/> {this.props.pillar}</div>
  }
}

PillarLabel.propTypes = {
  status: PropTypes.string,
  pillar: PropTypes.string
};
