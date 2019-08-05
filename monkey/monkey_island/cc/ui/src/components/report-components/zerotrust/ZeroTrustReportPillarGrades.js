import React, {Component} from "react";
import ZeroTrustPillars from "./ZeroTrustPillars";
import ZeroTrustReportFindingsTable from "./ZeroTrustReportFindingsTable";

export class ZeroTrustReportPillarGrades extends Component {
  render() {
    let pillarsCounters = {};
    for(const pillar in ZeroTrustPillars) {
      pillarsCounters[ZeroTrustPillars[pillar]] = {
        "conclusive": 0,
        "possible": 0
      };
    }

    if (this.props.findings !== null) {
      for (const finding of this.props.findings) {
        console.log("finding: " + JSON.stringify(finding));
        if (typeof finding === 'object' && finding !== null) {
          if (finding.hasOwnProperty("pillars") && finding.hasOwnProperty("conclusive")) {
            for (const pillar of finding["pillars"]) {
              if (finding.conclusive) {
                pillarsCounters[pillar]["conclusive"] += 1;
              } else {
                pillarsCounters[pillar]["possible"] += 1;
              }
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
