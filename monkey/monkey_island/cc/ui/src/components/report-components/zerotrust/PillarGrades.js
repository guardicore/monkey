import React, {Component} from "react";
import ZeroTrustPillars from "./ZeroTrustPillars";

export class PillarGrades extends Component {
  render() {
    return (
      <div id="pillar-grades">
        <p>
          TODO: table with conditional colouring.
        </p>
        <pre>
          {JSON.stringify(this.props.pillars, undefined, 2)}
        </pre>
      </div>
    )
  }
}

export default PillarGrades;
