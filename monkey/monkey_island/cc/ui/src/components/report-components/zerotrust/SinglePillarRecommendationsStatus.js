import AuthComponent from "../../AuthComponent";
import {PillarLabel} from "./PillarLabel";
import RecommendationsStatusTable from "./RecommendationsStatusTable";
import React from "react";

export class SinglePillarRecommendationsStatus extends AuthComponent {
  render() {
    return (
      <div>
        <h3><PillarLabel pillar={this.props.pillar}/></h3>
        <RecommendationsStatusTable recommendationStatus={this.props.recommendationStatus}/>
      </div>
    );
  }
}
