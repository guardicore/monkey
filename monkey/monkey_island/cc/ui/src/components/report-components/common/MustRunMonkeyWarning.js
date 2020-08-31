import React, {Component} from 'react';
import {NavLink} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons/faExclamationTriangle';

export default class MustRunMonkeyWarning extends Component {
  render() {
    return <p className="alert alert-warning">
      <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
      <b>You have to <NavLink to="/run-monkey">run a monkey</NavLink> before generating a report!</b>
    </p>
  }
}
