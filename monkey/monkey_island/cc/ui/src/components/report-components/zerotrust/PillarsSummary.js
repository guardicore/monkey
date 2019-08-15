import React, {Component, Fragment} from "react";
import {PillarLabel} from "./PillarLabel";

export class PillarsSummary extends Component {
  render() {
    return (<div id="piilar-summary">
      {this.getStatusSummary("Conclusive")}
      {this.getStatusSummary("Inconclusive")}
      {this.getStatusSummary("Positive")}
      {this.getStatusSummary("Unexecuted")}
    </div>);
  }

  getStatusSummary(status) {
    console.log(this.props.pillars);
    if (this.props.pillars[status].length > 0) {
      return <Fragment>
        <h3>{status}</h3>
        <div>
            {
              this.props.pillars[status].map((pillar) => {
                return <PillarLabel key={pillar} pillar={pillar}/>
              })
            }
        </div>
      </Fragment>
    }
  }
}
