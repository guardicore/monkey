import AuthComponent from "../../AuthComponent";
import PillarLabel from "./PillarLabel";
import RecommendationsStatusTable from "./RecommendationsStatusTable";
import React from "react";
import * as PropTypes from "prop-types";
import {Panel} from "react-bootstrap";

export default class SinglePillarRecommendationsStatus extends AuthComponent {
  render() {
    if (this.props.recommendationsStatus.length === 0) {
      return null;
    }
    else {
      return (
        <Panel>
          <Panel.Heading>
            <Panel.Title toggle>
              <h3 style={{textAlign: "center", marginTop: "1px", marginBottom: "1px"}}>
                <i className="fa fa-chevron-down" /> <PillarLabel pillar={this.props.pillar} status={this.props.pillarsToStatuses[this.props.pillar]} />
              </h3>
            </Panel.Title>
          </Panel.Heading>
          <Panel.Collapse>
            <Panel.Body>
              <RecommendationsStatusTable recommendationsStatus={this.props.recommendationsStatus}/>
            </Panel.Body>
          </Panel.Collapse>
        </Panel>
      );
    }
  }
}

SinglePillarRecommendationsStatus.propTypes = {
  recommendationsStatus: PropTypes.array,
  pillar: PropTypes.string,
};
