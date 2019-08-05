import React, {Component} from "react";
import ZeroTrustPillars from "./ZeroTrustPillars";

export class ZeroTrustReportPillarGrades extends Component {
  render() {
    let pillarsCounters = {};
    for(const pillar in ZeroTrustPillars){
      pillarsCounters[ZeroTrustPillars[pillar]] = 0;
    }

    if (this.props.findings !== null) {
      for (const finding of this.props.findings) {
        console.log("finding: " + JSON.stringify(finding));
        if (typeof finding === 'object' && finding !== null) {
          if (finding.hasOwnProperty("pillars")) {
            for (const pillar of finding["pillars"]) {
              pillarsCounters[pillar] = pillarsCounters[pillar] + 1;
            }
          }
        }
      }
    }

    return (
      <div id="pillar-grades">
        <p>
          TODO: table with conditional colouring.
        </p>
        <pre>
          {JSON.stringify(pillarsCounters, undefined, 2)}
        </pre>
      </div>
    )
  }
}

export default ZeroTrustReportPillarGrades;
