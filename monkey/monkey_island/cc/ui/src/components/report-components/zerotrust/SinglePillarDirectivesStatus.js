import AuthComponent from "../../AuthComponent";
import PillarLabel from "./PillarLabel";
import DirectivesStatusTable from "./DirectivesStatusTable";
import React, {Fragment} from "react";
import * as PropTypes from "prop-types";

export class SinglePillarDirectivesStatus extends AuthComponent {
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

SinglePillarDirectivesStatus.propTypes = {
  directivesStatus: PropTypes.array,
  pillar: PropTypes.string,
};
