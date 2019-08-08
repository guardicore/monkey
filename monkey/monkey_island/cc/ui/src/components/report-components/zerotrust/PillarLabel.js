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

    const className = "label " + pillarToColor[this.props.pillar];
    return <span className={className} style={{margin: '2px'}}>{this.props.pillar}</span>
  }
}
