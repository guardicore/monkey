import AuthComponent from "../../AuthComponent";
import {PillarLabel} from "./PillarLabel";
import DirectivesStatusTable from "./DirectivesStatusTable";
import React, {Fragment} from "react";

export class SinglePillarDirectivesStatus extends AuthComponent {
  directivesStatus;

  render() {
    if (this.props.directivesStatus.length === 0) {
      return null;
    }
    else {
      return (
        <Fragment>
          <h3><PillarLabel pillar={this.props.pillar} status={this.props.pillarsToStatuses[this.props.pillar]} /></h3>
          <DirectivesStatusTable directivesStatus={this.props.directivesStatus}/>
        </Fragment>
      );
    }
  }
}
