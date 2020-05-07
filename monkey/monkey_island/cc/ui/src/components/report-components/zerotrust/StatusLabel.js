import React, {Component} from 'react';
import * as PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheck } from '@fortawesome/free-solid-svg-icons/faCheck';
import { faExclamationTriangle } from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';
import { faBomb } from '@fortawesome/free-solid-svg-icons/faBomb';
import { faQuestion } from '@fortawesome/free-solid-svg-icons/faQuestion';

const statusToIcon = {
  'Passed': faCheck,
  'Verify': faExclamationTriangle,
  'Failed': faBomb,
  'Unexecuted': faQuestion
};

export const statusToLabelType = {
  'Passed': 'label-success',
  'Verify': 'label-warning',
  'Failed': 'label-danger',
  'Unexecuted': 'label-default'
};

export default class StatusLabel extends Component {
  render() {
    let text = '';
    if (this.props.showText) {
      text = ' ' + this.props.status;
    }

    return (
      <div className={'label ' + statusToLabelType[this.props.status]} style={{display: 'flow-root'}}>
        <FontAwesomeIcon icon={statusToIcon[this.props.status]} size={this.props.size}/>{text}
      </div>
    );
  }
}

StatusLabel.propTypes = {
  status: PropTypes.string,
  showText: PropTypes.bool,
  size: PropTypes.string
};
