import React, {Component, Fragment} from 'react';
import * as PropTypes from 'prop-types';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {faCheck, faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';

export default class SecurityIssuesGlance extends Component {
  render() {
    return <Fragment>
      {
        this.props.issuesFound ?
          (<p className="alert alert-danger">
            <FontAwesomeIcon icon={faExclamationTriangle} style={{'marginRight': '5px'}}/>
            Critical security issues were detected!
          </p>) :
          (<p className="alert alert-success">
            <FontAwesomeIcon icon={faCheck} style={{'marginRight': '5px'}}/>
            No critical security issues were detected.
          </p>)
      }
    </Fragment>
  }
}

SecurityIssuesGlance.propTypes = {issuesFound: PropTypes.bool};
