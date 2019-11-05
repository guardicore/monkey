import React, {Component} from "react";
import {statusToLabelType} from "./StatusLabel";
import * as PropTypes from "prop-types";

const pillarToIcon = {
  "Data": "fa fa-database",
  "People": "fa fa-user",
  "Networks": "fa fa-wifi",
  "Workloads": "fa fa-cloud",
  "Devices": "fa fa-laptop",
  "Visibility & Analytics": "fa fa-eye-slash",
  "Automation & Orchestration": "fa fa-cogs",
};

export default class PillarLabel extends Component {
  render() {
    const className = "label " + statusToLabelType[this.props.status];
    return <div className={className} style={{margin: '2px', display: 'inline-block'}}><i
      className={pillarToIcon[this.props.pillar]}/> {this.props.pillar}</div>
  }
}

PillarLabel.propTypes = {
  status: PropTypes.string,
  pillar: PropTypes.string,
};
