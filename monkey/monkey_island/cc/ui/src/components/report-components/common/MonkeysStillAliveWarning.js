import React, {Component} from 'react';
import * as PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';

export default class MonkeysStillAliveWarning extends Component {
  render() {
    return <div>
      {
        this.props.allMonkeysAreDead ?
          ''
          :
          (<p className="alert alert-warning">
            <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
            Some monkeys are still running. To get the best report it's best to wait for all of them to finish
            running.
          </p>)
      }
    </div>
  }
}

MonkeysStillAliveWarning.propTypes = {allMonkeysAreDead: PropTypes.bool};
