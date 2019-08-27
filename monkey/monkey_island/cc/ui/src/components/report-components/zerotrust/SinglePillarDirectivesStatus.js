import AuthComponent from "../../AuthComponent";
import PillarLabel from "./PillarLabel";
import DirectivesStatusTable from "./DirectivesStatusTable";
import React, {Fragment} from "react";
import * as PropTypes from "prop-types";
import {Panel} from "react-bootstrap";

export default class SinglePillarDirectivesStatus extends AuthComponent {
  render() {
    if (this.props.directivesStatus.length === 0) {
      return null;
    }
    else {
      return (
        <Panel>
          <Panel.Heading>
            <Panel.Title toggle>
              <h3 style={{"text-align": "center"}}>
                🔽 <PillarLabel pillar={this.props.pillar} status={this.props.pillarsToStatuses[this.props.pillar]} />
              </h3>
            </Panel.Title>
          </Panel.Heading>
          <Panel.Collapse>
            <Panel.Body>
              <DirectivesStatusTable directivesStatus={this.props.directivesStatus}/>
            </Panel.Body>
          </Panel.Collapse>
        </Panel>
      );
    }
  }
}

SinglePillarDirectivesStatus.propTypes = {
  directivesStatus: PropTypes.array,
  pillar: PropTypes.string,
};
