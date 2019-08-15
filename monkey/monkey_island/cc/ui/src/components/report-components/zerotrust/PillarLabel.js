import React, {Component} from "react";
import 'styles/ZeroTrustPillars.css'
import {statusToLabelType} from "./StatusLabel";

export class PillarLabel extends Component {
  pillar;
  status;

  render() {
    const pillarToIcon = {
      "Data": "fa fa-database",
      "People": "fa fa-user",
      "Networks": "fa fa-wifi",
      "Workloads": "fa fa-cloud",
      "Devices": "fa fa-laptop",
      "Visibility & Analytics": "fa fa-eye-slash",
      "Automation & Orchestration": "fa fa-cogs",
    };

    const className = "label " + statusToLabelType[this.props.status];
    return <div className={className} style={{margin: '2px', display: 'inline-block'}}><i className={pillarToIcon[this.props.pillar]}/> {this.props.pillar}</div>
  }
}
