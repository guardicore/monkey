import React, {Component} from "react";
import 'styles/ZeroTrustPillars.css'

export class PillarLabel extends Component {
  pillar;

  render() {
    const pillarToColor = {
      "Data": "label-zt-data",
      "People": "label-zt-people",
      "Networks": "label-zt-networks",
      "Workloads": "label-zt-workloads",
      "Devices": "label-zt-devices",
      "Visibility & Analytics": "label-zt-analytics",
      "Automation & Orchestration": "label-zt-automation",
    };

    const pillarToIcon = {
      "Data": "fa fa-database",
      "People": "fa fa-user",
      "Networks": "fa fa-wifi",
      "Workloads": "fa fa-cloud",
      "Devices": "fa fa-laptop",
      "Visibility & Analytics": "fa fa-eye-slash",
      "Automation & Orchestration": "fa fa-cogs",
    };

    const className = "label " + pillarToColor[this.props.pillar];
    return <div className={className} style={{margin: '2px', display: 'inline-block'}}><i className={pillarToIcon[this.props.pillar]}/> {this.props.pillar}</div>
  }
}
