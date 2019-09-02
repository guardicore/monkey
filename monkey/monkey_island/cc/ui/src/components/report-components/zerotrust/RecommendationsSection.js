import React, {Component} from "react";
import SinglePillarRecommendationsStatus from "./SinglePillarRecommendationsStatus";
import * as PropTypes from "prop-types";

export default class RecommendationsSection extends Component {
  render() {

    return <div id="recommendations-overview">
      <h2>Recommendations</h2>
      <p>
        Analyze each zero trust recommendation by pillar, and see if you've followed through with it. See test results
        to understand how the monkey tested your adherence to that recommendation.
      </p>
      {
        Object.keys(this.props.recommendations).map((pillar) =>
          <SinglePillarRecommendationsStatus
            key={pillar}
            pillar={pillar}
            recommendationsStatus={this.props.recommendations[pillar]}
            pillarsToStatuses={this.props.pillarsToStatuses}/>
        )
      }
    </div>
  }
}

RecommendationsSection.propTypes = {
  recommendations: PropTypes.any,
  pillarsToStatuses: PropTypes.any
};
