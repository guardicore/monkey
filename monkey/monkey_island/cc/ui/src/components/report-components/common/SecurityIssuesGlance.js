import React, {Component, Fragment} from "react";
import * as PropTypes from "prop-types";

export class SecurityIssuesGlance extends Component {
  render() {
    return <Fragment>
      {
        this.props.issuesFound ?
          (<p className="alert alert-danger">
            <i className="glyphicon glyphicon-exclamation-sign" style={{'marginRight': '5px'}}/>
            Critical security issues were detected!
          </p>) :
          (<p className="alert alert-success">
            <i className="glyphicon glyphicon-ok-sign" style={{'marginRight': '5px'}}/>
            No critical security issues were detected.
          </p>)
      }
    </Fragment>
  }
}

SecurityIssuesGlance.propTypes = {issuesFound: PropTypes.bool};
