import React, {Component} from "react";
import {NavLink} from "react-router-dom";

export default class MustRunMonkeyWarning extends Component {
  render() {
    return <p className="alert alert-warning">
      <i className="glyphicon glyphicon-warning-sign" style={{'marginRight': '5px'}}/>
      <b>You have to <NavLink to="/run-monkey">run a monkey</NavLink> before generating a report!</b>
    </p>
  }
}
